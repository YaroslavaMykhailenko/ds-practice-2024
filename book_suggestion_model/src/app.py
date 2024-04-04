import grpc
from concurrent import futures
import json
import numpy as np
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.pb.book_suggestion_model import book_suggestion_model_pb2
from utils.pb.book_suggestion_model import book_suggestion_model_pb2_grpc


from tools.logging import setup_logger
from tools.vectorclock.VectorClock import VectorClock

logger = setup_logger("book_suggestion_model")


from pymongo import MongoClient
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@mongo:27017/bookstore')
client = MongoClient(MONGO_URI)
db = client['bookstore']


class BookSuggestionModel:
    def __init__(self):
        # fetch the books from db.
        self.books = list(db.books.find({}))
        
        # self.titles = ["Learning Python", "Advanced Python", "Python Data Science", "Machine Learning with Python"]
        self.titles = [book["title"] for book in self.books]
        
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.titles)


    def get_similar_books(self, title, topk=1):
        # every title is a vector now, and we find the most similar by cos in the embed space.
        title_vec = self.vectorizer.transform([title])
        cosine_similarities = cosine_similarity(title_vec, self.tfidf_matrix)
        similar_indices = cosine_similarities[0].argsort()[::-1][1:topk+1]
        print(similar_indices, cosine_similarities[0].argsort())
        
        # logging.
        ranks = {self.titles[i]: np.round(cosine_similarities[0][i], 3) 
                 for i in cosine_similarities[0].argsort()}
        logger.info(ranks)

        return [self.books[i] for i in similar_indices]

model = BookSuggestionModel()


class BookSuggestionModelService(book_suggestion_model_pb2_grpc.BookSuggestionModelServiceServicer):
    def GetBookRecommendations(self, request, context):
        order = json.loads(request.order_json)
        global_clock_dict = json.loads(request.vector_clock_json)
        global_clock = VectorClock(global_clock_dict)

        local_clock = VectorClock()
        local_clock.initialize(list(global_clock.get_clock().keys()))

        # TODO: logic for checking the global state of a vector clock
        if not self.CheckGlobalClock(global_clock):
            logger.info(f"Invalid sequence of operations")
            # Here is question what better to return 
            return book_suggestion_model_pb2.BookRecommendations(books=[], vector_clock_json=json.dumps(global_clock.get_clock()))
        
        local_clock.increment("book_suggestion_model")
        print(f"LOCAL VECTOR CLOCK IN BOOK SUGGESTION MODEL: {local_clock.get_clock()}")

        global_clock.merge(local_clock.get_clock())

        print(f"GLOBAL VECTOR CLOCK IN BOOK SUGGESTION MODEL: {global_clock.get_clock()}")

        # get the ordered book title.
        book_title = order.get("items", [{}])[0].get("title", "")
        similar_books = model.get_similar_books(book_title, topk=2)

        books = [
            book_suggestion_model_pb2.Book(
                id=book.get("id", ""),
                title=book.get("title", ""),
                author=book.get("author", ""),
                description=book.get("description", ""),
                copies=book.get("copies", ""),
                copiesAvailable=book.get("copiesAvailable", ""),
                category=book.get("category", ""),
                img=book.get("img", ""),
                price=book.get("price", "")
            ) for book in similar_books
        ]

        return book_suggestion_model_pb2.BookRecommendations(books=books, vector_clock_json=json.dumps(global_clock.get_clock()))
    
    def CheckGlobalClock(self, global_clock):
        # ....
        return True

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_suggestion_model_pb2_grpc.add_BookSuggestionModelServiceServicer_to_server(BookSuggestionModelService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()