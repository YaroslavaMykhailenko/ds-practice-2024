from utils.pb.fraud_detection import fraud_detection_pb2, fraud_detection_pb2_grpc
from utils.pb.transaction_verification import transaction_verification_pb2, transaction_verification_pb2_grpc
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc

import grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import uuid

from tools.logging import setup_logger
from tools.vectorclock.VectorClock import VectorClock

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
    print(books)
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
    
def assign_order_id(order_details):
    order_details["orderId"] = str(uuid.uuid4())

@app.route('/checkout', methods=['POST'])
def checkout():
    order_details = request.json
    # print('Я ТУТ',order_details)
    
    if not order_details:
        return jsonify({'error': 'Invalid request'}), 400

    global_clock = VectorClock()
    global_clock.initialize(["transaction_verification", "fraud_detection", "suggestions", "book_suggestion_model"])
    print(f"GLOBAL VECTOR CLOCK IN ORCHESTRATOR: {global_clock.get_clock()}")

    vector_clock_json = json.dumps(global_clock.get_clock())

    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(channel)
        transaction_request = transaction_verification_pb2.TransactionVerificationRequest(order_json=json.dumps(order_details), vector_clock_json=vector_clock_json)
        transaction_response = stub.VerifyTransaction(transaction_request)
    
    response_data = json.loads(transaction_response.response_json)

    if response_data["status"] == "Order Approved":
        assign_order_id(response_data)        
        return jsonify({
            'orderId': response_data.get('orderId', 'Unknown'),
            'status': response_data["status"],
            'suggestedBooks': response_data["suggestedBooks"]
        }), 200
    else:
        return jsonify({
            'orderId': response_data.get('orderId', 'Unknown'), 
            'status': response_data["status"], 
            'suggestedBooks': response_data["suggestedBooks"]
        }), 200
  
    



if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
