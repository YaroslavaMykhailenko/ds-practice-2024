import grpc
from concurrent import futures
import json
import os

from utils.pb.suggestions import suggestions_pb2
from utils.pb.suggestions import suggestions_pb2_grpc

from utils.pb.book_suggestion_model import book_suggestion_model_pb2
from utils.pb.book_suggestion_model import book_suggestion_model_pb2_grpc

from tools.logging import setup_logger
from tools.vectorclock.VectorClock import VectorClock

logger = setup_logger("suggestions")


from pymongo import MongoClient
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@mongo:27017/bookstore')
client = MongoClient(MONGO_URI)
db = client['bookstore']


class SuggestionsService(suggestions_pb2_grpc.SuggestionsServiceServicer):
    def GetSuggestions(self, request, context):

        order = json.loads(request.order_json)
        global_clock_dict = json.loads(request.vector_clock_json)
        global_clock = VectorClock(global_clock_dict)

        local_clock = VectorClock()
        local_clock.initialize(list(global_clock.get_clock().keys()))

        # TODO: logic for checking the global state of a vector clock
        if not self.CheckGlobalClock(global_clock):
            logger.info(f"Invalid sequence of operations")
            # Here is question what better to return 
            return suggestions_pb2.SuggestionsResponse(suggestions=[], vector_clock_json=json.dumps(global_clock.get_clock()))
        
        local_clock.increment("suggestions")
        print(f"LOCAL VECTOR CLOCK IN SUGGESTIONS SERVICE: {local_clock.get_clock()}")

        global_clock.merge(local_clock.get_clock())
        print(f"GLOBAL VECTOR CLOCK IN SUGGESTIONS SERVICE: {global_clock.get_clock()}")
        order_json = json.dumps(order)

        with grpc.insecure_channel('book_suggestion_model:50054') as channel:
            stub = book_suggestion_model_pb2_grpc.BookSuggestionModelServiceStub(channel)
            request = book_suggestion_model_pb2.RecommendationsRequest(order_json=order_json, vector_clock_json=json.dumps(global_clock.get_clock()))
            recommendations = stub.GetBookRecommendations(request)
                
        suggestions = [
            suggestions_pb2.Book(
                id=rec.id,
                title=rec.title,
                author=rec.author,
                description=rec.description,
                copies=rec.copies,
                copiesAvailable=rec.copiesAvailable,
                category=rec.category,
                img=rec.img,
                price=rec.price
            ) for rec in recommendations.books
        ]

        return suggestions_pb2.SuggestionsResponse(suggestions=suggestions, vector_clock_json=json.dumps(global_clock.get_clock()))

    def CheckGlobalClock(self, global_clock):
        # ....
        return True
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_pb2_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
