import grpc

import sys
sys.path.append("./")
from utils.pb.fraud_detection import fraud_detection_pb2
from utils.pb.fraud_detection import fraud_detection_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = fraud_detection_pb2_grpc.HelloServiceStub(channel)
    response = stub.SayHello(fraud_detection_pb2.HelloRequest(name='World'))
    print("gRPC client received: " + response.greeting)

if __name__ == '__main__':
    run()
