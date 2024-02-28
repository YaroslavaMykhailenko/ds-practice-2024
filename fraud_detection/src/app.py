import grpc
from concurrent import futures
import json

from utils.pb.fraud_detection import fraud_detection_pb2
from utils.pb.fraud_detection import fraud_detection_pb2_grpc

from tools.logging import setup_logger
logger = setup_logger("fraud_detection")


class FraudDetectionService(fraud_detection_pb2_grpc.FraudDetectionServiceServicer):
    # ref: https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
    def CheckFraud(self, request, context):
        order = json.loads(request.order_json)
        logger.info("FraudDetectionService logic should come here!")

        is_fraudulent = False
        return fraud_detection_pb2.FraudCheckResponse(is_fraudulent=is_fraudulent)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()