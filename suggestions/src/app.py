import grpc
from concurrent import futures
import json

from utils.pb.suggestions import suggestions_pb2
from utils.pb.suggestions import suggestions_pb2_grpc

from tools.logging import setup_logger
logger = setup_logger("suggestions")


class SuggestionsService(suggestions_pb2_grpc.SuggestionsServiceServicer):
    def GetSuggestions(self, request, context):
        order = json.loads(request.order_json)
        logger.info("SuggestionsService logic should come here!")

        # db connection 
        suggestions = [
            suggestions_pb2.Book(id="1001", 
                                 title="Learning Python", 
                                 author="Mark Lutz", 
                                 description="", 
                                 img="", 
                                 price=40
                                 ),
        ]
        return suggestions_pb2.SuggestionsResponse(suggestions=suggestions)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_pb2_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
