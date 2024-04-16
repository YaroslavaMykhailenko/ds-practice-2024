from utils.pb.fraud_detection import fraud_detection_pb2, fraud_detection_pb2_grpc
from utils.pb.transaction_verification import transaction_verification_pb2, transaction_verification_pb2_grpc
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc
from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.pb.order_executor import order_executor_pb2, order_executor_pb2_grpc

import grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import uuid

from tools.logging import setup_logger
logger = setup_logger("orchestrator")

app = Flask(__name__)
CORS(app)


from pymongo import MongoClient
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@mongo:27017/bookstore')
client = MongoClient(MONGO_URI)
db = client['bookstore']


# TODO: these functions should be outside
@app.route('/api/books', methods=['GET'])
def get_books():
    books_cursor = db.books.find({})
    books = list(books_cursor)
    # print(books)
    for book in books:
        book['_id'] = str(book['_id'])

    if books:
        return jsonify(books)
    else:
        return jsonify({"error": "Books not found"}), 404


@app.route('/api/books/<bookId>', methods=['GET'])
def get_book(bookId):
    book = db.books.find_one({"id": bookId}, {'_id': 0})
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404
    



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


def enqueue_order(order_details):
    channel = grpc.insecure_channel('order_queue:50055')
    stub = order_queue_pb2_grpc.OrderQueueServiceStub(channel)
    
    assign_order_id(order_details)
    order_json = json.dumps(order_details)
    priority = int(sum(item['price'] * item['quantity'] for item in order_details['items']))
    response = stub.Enqueue(order_queue_pb2.Order(order_json=order_json, priority=priority))
    
    logger.info(f"Order enqueue success: {response.success}")


# import random
# def process_orders():
#     # channel = grpc.insecure_channel('order_executor:50056')

#     # stub = order_executor_pb2_grpc.OrderExecutorServiceStub(channel)
    
#     # try:
#     #     response = stub.ProcessOrder(order_executor_pb2.ProcessOrderRequest())
#     #     print(f"Response from executor: {response.message}")
#     # except grpc.RpcError as e:
#     #     print(f"Failed to process order: {e}")

#     executors = ['order_executor_1:50056', 'order_executor_2:50056']
#     selected_executor = random.choice(executors)

#     channel = grpc.insecure_channel(selected_executor)
#     stub = order_executor_pb2_grpc.OrderExecutorServiceStub(channel)
    
#     try:
#         response = stub.ProcessOrder(order_executor_pb2.ProcessOrderRequest())
#         print(f"Response from executor: {response.message}")
#     except grpc.RpcError as e:
#         print(f"Failed to process order with {selected_executor}: {e}")
    


# REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
# REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
# INSTANCE_INFO_KEY = 'executor_instances'
# LEADER_KEY = 'order_executor_leader'
# HEARTBEAT_EXPIRE = 10

# import random
# import redis
# import time 


# def get_available_services():
#     redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
#     services = json.loads(redis_client.get(INSTANCE_INFO_KEY) or "{}")
#     print(f"all executor services: {services}")
#     print()

#     # filter services based on timeout-thr for heartbeats.
#     print({svc: time.time() - details["last_heartbeat"] for svc, details in services.items()})
#     return [details for svc, details in services.items() if time.time() - details["last_heartbeat"] < HEARTBEAT_EXPIRE]


# def process_orders():
#     available_executors = get_available_services()
    
#     if not available_executors:
#         print("No available executors.")
#         return

#     selected_executor = random.choice(available_executors)
#     address = selected_executor["address"]
#     print(f"selected_executor: {selected_executor}")

#     channel = grpc.insecure_channel(address)
#     stub = order_executor_pb2_grpc.OrderExecutorServiceStub(channel)
    
#     try:
#         response = stub.ProcessOrder(order_executor_pb2.ProcessOrderRequest())
#         print(f"Response from executor: {response.message}")
#     except grpc.RpcError as e:
#         print(f"Failed to process order with {selected_executor}: {e}")
    


# def process_orders():
#     redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
#     leader = redis_client.get(LEADER_KEY)
    
#     if not leader:
#         print("No leader available.")
#         return

#     # Decode the leader ID to get its address from the instance registry
#     leader_id = leader.decode()
#     instances = json.loads(redis_client.get(INSTANCE_INFO_KEY) or "{}")
#     leader_address = instances[leader_id]["address"]

#     print(f"Leader selected: {leader_id} with address {leader_address}")
#     print({svc: time.time() - details["last_heartbeat"] for svc, details in instances.items()})

#     channel = grpc.insecure_channel(leader_address)
#     stub = order_executor_pb2_grpc.OrderExecutorServiceStub(channel)
    
#     try:
#         response = stub.ProcessOrder(order_executor_pb2.ProcessOrderRequest())
#         print(f"Response from leader: {response.message}")
#     except grpc.RpcError as e:
#         print(f"Failed to process order with {leader_id}: {e}")




from order_executor.src.app import get_leader

def process_orders():
    leader_address = get_leader()

    try:
        channel = grpc.insecure_channel(leader_address)
        stub = order_executor_pb2_grpc.OrderExecutorServiceStub(channel)
        response = stub.ProcessOrder(order_executor_pb2.ProcessOrderRequest())
        print(f"Response from executor: {response.message}")
    except grpc.RpcError as e:
        print(f"Failed to process order with executor at {leader_address}: {e}")




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


def assign_order_id(order_details):
    order_details["orderId"] = str(uuid.uuid4())


def process_order(order_details):
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





@app.route('/checkout', methods=['POST'])
def checkout():
    order_details = request.json
    print(order_details)
    
    if not order_details:
        return jsonify({'error': 'Invalid request'}), 400


    # might merge the responses.
    # if results["is_fraudulent"]:
    #     return jsonify({
    #         'orderId': order_details.get('orderId', 'Unknown'), 
    #         'status': 'Order Rejected', 
    #         'suggestedBooks': []
    #     }), 200
    
    # if not results["is_valid"]:
    #     return jsonify({
    #         'orderId': order_details.get('orderId', 'Unknown'), 
    #         'status': 'Order Rejected', 
    #         'suggestedBooks': []
    #     }), 200
    
    # TODO: encapsulate order processing logic.
    enqueue_order(order_details)
    process_orders()

    # results = process_order(order_details)

    return jsonify({
        'orderId': order_details.get('orderId', 'Unknown'),
        'status': 'Order Approved',
        'suggestedBooks': results["suggested_books"]
    }), 200



if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
