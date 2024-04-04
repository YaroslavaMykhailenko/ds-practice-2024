import grpc
from concurrent import futures
import json
from datetime import datetime, timedelta

from utils.pb.fraud_detection import fraud_detection_pb2
from utils.pb.fraud_detection import fraud_detection_pb2_grpc
from utils.pb.suggestions import suggestions_pb2_grpc
from utils.pb.suggestions import suggestions_pb2
import uuid
from tools.logging import setup_logger
from tools.vectorclock.VectorClock import VectorClock
logger = setup_logger("fraud_detection")


class FraudDetectionService(fraud_detection_pb2_grpc.FraudDetectionServiceServicer):
    # ref: https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
    def CheckFraud(self, request, context):
        order = json.loads(request.order_json)
        global_clock_dict = json.loads(request.vector_clock_json)
        global_clock = VectorClock(global_clock_dict)

        local_clock = VectorClock()
        local_clock.initialize(list(global_clock.get_clock().keys()))
        
        # TODO: logic for checking the global state of a vector clock
        if not self.CheckGlobalClock(global_clock):
            logger.info(f"Invalid sequence of operations")
            response_json = {"orderId": order.get('orderId', 'Unknown'), "status": "Order Rejected", "suggestedBooks": []}
            return fraud_detection_pb2.FraudCheckResponse(response_json=json.dumps(response_json), vector_clock_json=json.dumps(global_clock.get_clock()))
        
        local_clock.increment("fraud_detection")
        print(f"LOCAL VECTOR CLOCK IN FRAUD DETECTION: {local_clock.get_clock()}")

        if self.check_credit_card_expiration(order['creditCard']['expirationDate']):
            response_json = {"orderId": order.get('orderId', 'Unknown'), "status": "Order Rejected", "suggestedBooks": []}
            return fraud_detection_pb2.FraudCheckResponse(response_json=json.dumps(response_json), vector_clock_json=json.dumps(global_clock.get_clock()))
        
        global_clock.merge(local_clock.get_clock())
        print(f"GLOBAL VECTOR CLOCK IN FRAUD DETECTION: {global_clock.get_clock()}")

        suggestions, vector_clock_json = self.call_suggestions_service(order, global_clock.get_clock())
        vector_clock_json = json.loads(vector_clock_json)
        
        # self.assign_order_id(order)
        response_json = {"orderId": order.get('orderId', 'Unknown'), "status": "Order Approved", "suggestedBooks": suggestions}

        return fraud_detection_pb2.FraudCheckResponse(response_json=json.dumps(response_json), vector_clock_json=json.dumps(vector_clock_json))
    
    def check_credit_card_expiration(self, expire_date):
        try:
            expiration_date = datetime.strptime(expire_date, '%m/%y')
            one_month_ahead = datetime.now() + timedelta(days=30)
            
            if expiration_date < datetime.now() or expiration_date <= one_month_ahead:
                return True
            
        except ValueError as e:
            logger.error(f"Invalid expiration date format: {expire_date} - {e}")
            return True

        return False

    def CheckGlobalClock(self, global_clock):
        # ....
        return True
    
    # def assign_order_id(order_details):
    #     order_details["orderId"] = str(uuid.uuid4())
    
    
    def call_suggestions_service(self, order, vector_clock):
        with grpc.insecure_channel('suggestions:50053') as channel:
            stub = suggestions_pb2_grpc.SuggestionsServiceStub(channel)
            order_json = json.dumps(order)

            request = suggestions_pb2.SuggestionsRequest(order_json=order_json, vector_clock_json=json.dumps(vector_clock))
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

        return suggested_books, response.vector_clock_json
            


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()