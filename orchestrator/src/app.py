from utils.pb.fraud_detection import fraud_detection_pb2, fraud_detection_pb2_grpc
from utils.pb.transaction_verification import transaction_verification_pb2, transaction_verification_pb2_grpc
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc

import grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from tools.logging import setup_logger
logger = setup_logger("orchestrator")

app = Flask(__name__)
CORS(app)


def call_fraud_detection_service(order_details):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionServiceStub(channel)
        order_json = json.dumps(order_details)
        
        # TODO: need more secure ways for validating fraud
        request = fraud_detection_pb2.FraudCheckRequest(order_json=order_json)
        response = stub.CheckFraud(request)
        logger.info(f"is_fraudulent: {response.is_fraudulent}")

    return response.is_fraudulent


def call_transaction_verification_service(order_details):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationServiceStub(channel)
        order_json = json.dumps(order_details)

        request = transaction_verification_pb2.TransactionVerificationRequest(order_json=order_json)
        response = stub.VerifyTransaction(request)
        logger.info(f"is_valid: {response.is_valid}")

    return response.is_valid


def call_suggestions_service(order_details):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsServiceStub(channel)
        order_json = json.dumps(order_details)

        request = suggestions_pb2.SuggestionsRequest(order_json=order_json)
        response = stub.GetSuggestions(request)
        
        suggested_books = [
            {
                'bookId': book.id, 
                'title': book.title, 
                'author': book.author, 
                'description': book.description, 
                'img': book.img, 
                'price': book.price
            } for book in response.suggestions]

    
    logger.info(f"suggested_books: {suggested_books}")

    return suggested_books


@app.route('/checkout', methods=['POST'])
def checkout():
    order_details = request.json
    
    logger.info(order_details)

    if not order_details:
        return jsonify({'error': 'Invalid request'}), 400

    # fraud detection service.
    # TODO: merge + sync
    is_fraudulent = call_fraud_detection_service(order_details)
    if is_fraudulent:
        return jsonify({
            'orderId': order_details.get('orderId', 'Unknown'), 
            'status': 'Order Rejected', 
            'suggestedBooks': []
            }), 200

    # transaction validation service.
    is_valid = call_transaction_verification_service(order_details)
    if not is_valid:
        return jsonify({
            'orderId': order_details.get('orderId', 'Unknown'), 
            'status': 'Order Rejected', 
            'suggestedBooks': []
            }), 200
    
    # suggestions service.
    suggested_books = call_suggestions_service(order_details)

    # TODO: how do we generate oreder id?
    order_status_response = jsonify({
        'orderId': order_details.get('orderId', 'Unknown'),
        'status': 'Order Approved',
        'suggestedBooks': suggested_books
    }), 200

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
