import grpc
from concurrent import futures
import json
from datetime import datetime, timedelta

from utils.pb.fraud_detection import fraud_detection_pb2
from utils.pb.fraud_detection import fraud_detection_pb2_grpc

from tools.logging import setup_logger
import logging
logger = setup_logger("fraud_detection")


class FraudDetectionService(fraud_detection_pb2_grpc.FraudDetectionServiceServicer):
    # ref: https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
    def CheckFraud(self, request, context):

        order = json.loads(request.order_json)

        if self.check_credit_card_expiration(order['creditCard']['expirationDate']):
            return fraud_detection_pb2.FraudCheckResponse(is_fraudulent=True)
        
        return fraud_detection_pb2.FraudCheckResponse(is_fraudulent=False)
    
    def check_credit_card_expiration(self, expire_date):
        try:
            expiration_date = datetime.strptime(expire_date, '%m/%y')
            one_month_ahead = datetime.now() + timedelta(days=30)
            
           
            if expiration_date < datetime.now() or expiration_date <= one_month_ahead:
                return True
        except ValueError as e:
            
            logging.error(f"Invalid expiration date format: {expire_date} - {e}")
            return True

        return False



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()