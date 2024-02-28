import grpc
from concurrent import futures
import json

from utils.pb.transaction_verification import transaction_verification_pb2
from utils.pb.transaction_verification import transaction_verification_pb2_grpc

from tools.logging import setup_logger
logger = setup_logger("transaction_verification")


class TransactionVerificationService(transaction_verification_pb2_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        order = json.loads(request.order_json)
        logger.info("TransactionVerificationService logic should come here!")

        is_valid = True
        return transaction_verification_pb2.TransactionVerificationResponse(is_valid=is_valid)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServiceServicer_to_server(TransactionVerificationService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()