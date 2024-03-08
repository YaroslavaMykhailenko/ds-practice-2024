import grpc
from concurrent import futures
import json
import os

from utils.pb.suggestions import suggestions_pb2
from utils.pb.suggestions import suggestions_pb2_grpc

from utils.pb.book_suggestion_model import book_suggestion_model_pb2
from utils.pb.book_suggestion_model import book_suggestion_model_pb2_grpc

from tools.logging import setup_logger
logger = setup_logger("suggestions")


from pymongo import MongoClient
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@mongo:27017/bookstore')
client = MongoClient(MONGO_URI)
db = client['bookstore']


class SuggestionsService(suggestions_pb2_grpc.SuggestionsServiceServicer):
    def GetSuggestions(self, request, context):
        # order = json.loads(request.order_json)
        # # logger.info("SuggestionsService logic should come here!")

        # # db connection 
        # books_cursor = db.books.find({})
        # books = list(books_cursor)
        
        # suggestions = [
        #     suggestions_pb2.Book(
        #         id=book.get("id", ""),
        #         title=book.get("title", ""),
        #         author=book.get("author", ""),
        #         description=book.get("description", ""),
        #         copies=book.get("copies", ""),
        #         copiesAvailable=book.get("copiesAvailable", ""),
        #         category=book.get("category", ""),
        #         img=book.get("img", ""),
        #         price=book.get("price", "")
        #     ) for book in books
        # ]

        order = json.loads(request.order_json)
        order_json = json.dumps(order)

        with grpc.insecure_channel('book_suggestion_model:50054') as channel:
            stub = book_suggestion_model_pb2_grpc.BookSuggestionModelServiceStub(channel)
            request = book_suggestion_model_pb2.RecommendationsRequest(order_json=order_json)
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

        return suggestions_pb2.SuggestionsResponse(suggestions=suggestions)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_pb2_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
