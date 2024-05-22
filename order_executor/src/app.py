import grpc
import os
import redis
import time
import threading
from concurrent import futures
import json
import random

from utils.pb.fraud_detection import fraud_detection_pb2, fraud_detection_pb2_grpc
from utils.pb.transaction_verification import transaction_verification_pb2, transaction_verification_pb2_grpc
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc

from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.pb.order_executor import order_executor_pb2, order_executor_pb2_grpc

from utils.pb.payment import payment_pb2
from utils.pb.payment import payment_pb2_grpc

from utils.pb.book_storage import book_storage_pb2
from utils.pb.book_storage import book_storage_pb2_grpc

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
ORDER_QUEUE_SERVICE = 'order_queue:50055'
SERVICE_ID = os.getenv('SERVICE_ID', 'order_executor_' + str(os.getpid()))
INSTANCE_INFO_KEY = 'executor_instances'
LEADER_KEY = 'order_executor_leader'
HEARTBEAT_EXPIRE = 10
ELECTION_TIMEOUT = 2

print(SERVICE_ID)

from tools.logging import setup_logger
logger = setup_logger("order_executor")


def call_fraud_detection_service(order_details):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionServiceStub(channel)
        order_json = json.dumps(order_details)
        
        # TODO: need more secure ways for validating fraud
        request = fraud_detection_pb2.FraudCheckRequest(order_json=order_json)
        response = stub.CheckFraud(request)
        logger.info(f"is_fraudulent: {response.is_fraudulent}")

    return response.is_fraudulent


def call_transaction_verification_service(order_details):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(channel)
        order_json = json.dumps(order_details)

        request = transaction_verification_pb2.TransactionVerificationRequest(order_json=order_json)
        response = stub.VerifyTransaction(request)
        logger.info(f"is_valid: {response.is_valid}")

    return response.is_valid


def call_suggestions_service(order_details):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsServiceStub(channel)
        order_json = json.dumps(order_details)

        request = suggestions_pb2.SuggestionsRequest(order_json=order_json)
        response = stub.GetSuggestions(request)
        
        suggested_books = [
            {
                'bookId': book.id, 
                'title': book.title, 
                'author': book.author, 
                'description': book.description, 
                'copies': book.copies, 
                'copiesAvailable': book.copiesAvailable, 
                'category': book.category, 
                'img': book.img, 
                'price': book.price
            } for book in response.suggestions]
    
    logger.info(f"suggested_books: {suggested_books}")

    return suggested_books


# TEMP


def get_available_services(redis_client):
    services = json.loads(redis_client.get(INSTANCE_INFO_KEY) or "{}")
    # filter services based on timeout-thr for heartbeats.
    print({svc: time.time() - details["last_heartbeat"] for svc, details in services.items()})
    return {svc: details for svc, details in services.items() if time.time() - details["last_heartbeat"] < HEARTBEAT_EXPIRE}


def get_leader():
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    leader = redis_client.get(LEADER_KEY)
    instances = json.loads(redis_client.get(INSTANCE_INFO_KEY) or "{}")

    if leader and (leader in instances) and (time.time() - instances[leader]["last_heartbeat"] < HEARTBEAT_EXPIRE):
        leader_address = instances[leader]["address"]
    else:
        # leader is unavailable. we need to select a new one.
        available_executors = get_available_services(redis_client)
        if not available_executors:
            print("No available executors.")
            return

        leader_id, leader_info = random.choice(list(available_executors.items()))
        leader_address = leader_info["address"]
        print(f"New executor has been selected: {leader_id} with address: {leader_address}")

    return leader_address



class OrderExecutor(order_executor_pb2_grpc.OrderExecutorServiceServicer):
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.service_id = SERVICE_ID
        self.register_instance()
        self.start_heartbeat_thread()


    def register_instance(self):
        instances = json.loads(self.redis_client.get(INSTANCE_INFO_KEY) or '{}')
        instances[self.service_id] = {"address": f"{self.service_id}:50056", "last_heartbeat": time.time()}
        self.redis_client.set(INSTANCE_INFO_KEY, json.dumps(instances))


    def start_heartbeat_thread(self):
        def send_heartbeat():
            while True:
                self.register_instance()
                time.sleep(HEARTBEAT_EXPIRE / 2)
        thread = threading.Thread(target=send_heartbeat)
        thread.start()


    def is_leader_alive(self):
        leader = self.redis_client.get(LEADER_KEY)
        print(f"inernally shown last leader: {leader}")

        if leader:
            instances = json.loads(self.redis_client.get(INSTANCE_INFO_KEY) or '{}')
            leader_heartbeat = instances.get(leader, {}).get("last_heartbeat", 0)
            if time.time() - leader_heartbeat < HEARTBEAT_EXPIRE:
                return True
        return False
    

    def initiate_election(self):
        print(f"{self.service_id} is initiating an election.")
        instances = json.loads(self.redis_client.get(INSTANCE_INFO_KEY) or '{}')
        
        alive_instances = {id: data for id, data in instances.items() if time.time() - data["last_heartbeat"] < HEARTBEAT_EXPIRE}

        higher_ids = [id for id in alive_instances if id > self.service_id]
        if not higher_ids:
            self.declare_victory()
        else:
            for higher_id in higher_ids:
                # this could be direct communication or using a message broker.
                self.redis_client.hset("election_messages", higher_id, f"{self.service_id} challenges you")

            time.sleep(ELECTION_TIMEOUT)
            self.check_election_outcome(higher_ids)


    def declare_victory(self):
        print(f"{self.service_id} has won the election and is declaring itself the leader.")
        self.redis_client.set(LEADER_KEY, self.service_id)


    def check_election_outcome(self, higher_ids):
        new_leader = self.redis_client.get(LEADER_KEY)
        if new_leader and new_leader.decode() in higher_ids:
            print(f"{self.service_id} acknowledges new leader: {new_leader}")
        elif not new_leader:
            self.declare_victory()


    def get_leader_address(self):
        leader_id = self.redis_client.get(LEADER_KEY)
        if leader_id:
            instances = json.loads(self.redis_client.get(INSTANCE_INFO_KEY) or '{}')
            leader_info = instances.get(leader_id)
            if leader_info:
                return leader_info['address']
        return None


    def reroute_to_leader(self, leader_address, request):
        # forward the request to the leader.
        with grpc.insecure_channel(leader_address) as channel:
            stub = order_queue_pb2_grpc.OrderQueueServiceStub(channel)
            return stub.ProcessOrder(request)


    def ProcessOrder(self, request, context):
        print()
        print(f"currently on service: {self.service_id}")
        print(f"is_leader_alive: {self.is_leader_alive()}")

        if not self.is_leader_alive():
            self.initiate_election()

        leader_address = self.get_leader_address()

        print(f"leader_address: {leader_address}")
        print(f"selected leader: {self.redis_client.get(LEADER_KEY)}")
        print()

        if leader_address and self.redis_client.get(LEADER_KEY) == self.service_id:
            with grpc.insecure_channel(ORDER_QUEUE_SERVICE) as channel:
                stub = order_queue_pb2_grpc.OrderQueueServiceStub(channel)
                order = stub.Dequeue(order_queue_pb2.DequeueRequest())
                
                if order.id:
                    order_results = self._ProcessOrder(order)

                    # Check for fraud and validity before sending prepare requests.
                    is_fraudulent = order_results["is_fraudulent"]
                    is_valid = order_results["is_valid"]
                    
                    order_results = json.dumps(order_results)

                    if is_fraudulent or not is_valid:
                        logger.info(f"Order validation failed. Fraudulent: {is_fraudulent}, Valid: {is_valid}")
                        return order_executor_pb2.ProcessOrderResponse(success=False, order_json=order.order_json, order_result=order_results)

                    # Order is fine, prepare to commit transaction.
                    payment_result, db_result = self.HandleOrderTransaction(order)
                     
                    while payment_result.message == 'Abort' or db_result.message == 'Abort':
                        time.sleep(50)
                        payment_result, db_result = self.HandleOrderTransaction(order)

                    if payment_result.message == 'Commit' and db_result.message == 'Commit':
                        if payment_result.success and db_result.success: 
                            logger.info('Order processed successfully. Payment completed and db updated')
                            return order_executor_pb2.ProcessOrderResponse(success=True, order_json=order.order_json, order_result=order_results)
                        else:
                            logger.info('Order processed unsuccessfully. Error in payment or db commit')
                            return order_executor_pb2.ProcessOrderResponse(success=False, order_json=order.order_json, order_result={})
                else:
                    return order_executor_pb2.ProcessOrderResponse(success=False, order_json=order.order_json, order_result={})
        
        elif leader_address:
            print(f"Rerouting order to the leader at {leader_address}")
            return self.reroute_to_leader(leader_address, request)
        else:
            return order_executor_pb2.ProcessOrderResponse(success=False, order_json={}, order_result={})
        
    
    def _ProcessOrder(self, order):
        print(f"Leader {self.service_id} processed order {order.id}: {order.order_json}")
        
        order_details = json.loads(order.order_json)
        results = {}

        def fraud_detection_wrapper():
            logger.info(f"Starting proceess fraud_detection_service...")
            results["is_fraudulent"] = call_fraud_detection_service(order_details)

        def transaction_verification_wrapper():
            logger.info(f"Starting proceess transaction_verification_service...")
            results["is_valid"] = call_transaction_verification_service(order_details)

        def suggestions_wrapper():
            logger.info(f"Starting proceess suggestions_service...")
            results["suggested_books"] = call_suggestions_service(order_details)
            

        threads = [
            threading.Thread(target=fraud_detection_wrapper),
            threading.Thread(target=transaction_verification_wrapper),
            threading.Thread(target=suggestions_wrapper)
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        return results
    

    def HandleOrderTransaction(self, order):
        # Start 2PC        
        logger.info(f"2PC protocol...")
        logger.info(f"Executor sent 'prepare message' to services...")

        with grpc.insecure_channel('payment_service:50058') as channel:
            stub = payment_pb2_grpc.PaymentServiceStub(channel)
            prepare_payment_request = payment_pb2.PrepareRequest(order_id=order.id, order_details_json=order.order_json, message='VOTE_REQUEST')
            prepare_payment_response = stub.Prepare(prepare_payment_request)

        with grpc.insecure_channel('book_storage_1:50060') as channel:
            stub = book_storage_pb2_grpc.BookStorageStub(channel)
            prepare_book_request = book_storage_pb2.PrepareRequest(order_id=order.id, order_details_json=order.order_json, message='VOTE_REQUEST')
            prepare_book_response = stub.Prepare(prepare_book_request)
        
        if prepare_payment_response.willCommit and prepare_book_response.willCommit:
            logger.info(f"All services ready to commit!")
            logger.info(f"Executor sent 'global commit message' to services...")

            with grpc.insecure_channel('payment_service:50058') as channel:
                stub = payment_pb2_grpc.PaymentServiceStub(channel)
                commit_payment_request = payment_pb2.CommitRequest(order_id=order.id, message='GLOBAL_COMMIT')
                commit_payment_response = stub.Commit(commit_payment_request)
            
            with grpc.insecure_channel('book_storage_1:50060') as channel:
                stub = book_storage_pb2_grpc.BookStorageStub(channel)
                commit_book_request = book_storage_pb2.CommitRequest(order_id=order.id, message='GLOBAL_COMMIT')
                commit_book_response = stub.Commit(commit_book_request)

            return commit_payment_response, commit_book_response      
        else:
            logger.info(f"One of the services abort to commit!")
            logger.info(f"Executor sent 'global abort message' to services...")

            return self.AbortTransaction(order, 'Prepare Vote Failed')

    def AbortTransaction(self, order, reason):
        logger.info(f"Aborting transaction for order {order.id}: {reason}")

        with grpc.insecure_channel('payment_service:50058') as channel:
            stub = payment_pb2_grpc.PaymentServiceStub(channel)
            abort_payment_request = payment_pb2.AbortRequest(order_id=order.id, message='GLOBAL_ABORT')
            abort_payment_response = stub.Abort(abort_payment_request)

        print("Recieved ABORT from PaymentService")
        print()

        with grpc.insecure_channel('book_storage_1:50060') as channel:
            stub = book_storage_pb2_grpc.BookStorageStub(channel)
            abort_book_request = book_storage_pb2.AbortRequest(order_id=order.id, message='GLOBAL_ABORT')
            abort_book_response = stub.Abort(abort_book_request)

        print("Recieved ABORT from BookStorage")
        print()

        print(abort_payment_response)
        print(abort_book_response)

        return abort_payment_response, abort_book_response



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = OrderExecutor()
    order_executor_pb2_grpc.add_OrderExecutorServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50056')
    server.start()
    print(f"Service {SERVICE_ID} started.")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
