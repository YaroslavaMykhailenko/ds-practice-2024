from utils.pb.fraud_detection import fraud_detection_pb2, fraud_detection_pb2_grpc
from utils.pb.transaction_verification import transaction_verification_pb2, transaction_verification_pb2_grpc
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc
from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.pb.order_executor import order_executor_pb2, order_executor_pb2_grpc

import grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import uuid

from tools.logging import setup_logger
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
    # print(books)
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
    



def enqueue_order(order_details):
    channel = grpc.insecure_channel('order_queue:50055')
    stub = order_queue_pb2_grpc.OrderQueueServiceStub(channel)
    
    assign_order_id(order_details)
    order_json = json.dumps(order_details)
    priority = int(sum(item['price'] * item['quantity'] for item in order_details['items']))
    response = stub.Enqueue(order_queue_pb2.Order(order_json=order_json, priority=priority))
    
    logger.info(f"Order enqueue success: {response.success}")



# import sys
# sys.path.append("../../")
# from order_executor.src.app import get_leader

# =============== temp ===============
import redis
import time
import random

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
ORDER_QUEUE_SERVICE = 'order_queue:50055'
SERVICE_ID = os.getenv('SERVICE_ID', 'order_executor_' + str(os.getpid()))
INSTANCE_INFO_KEY = 'executor_instances'
LEADER_KEY = 'order_executor_leader'
HEARTBEAT_EXPIRE = 10
ELECTION_TIMEOUT = 2

print(SERVICE_ID)


def get_available_services(redis_client):
    services = json.loads(redis_client.get(INSTANCE_INFO_KEY) or "{}")
    # filter services based on timeout-thr for heartbeats.
    print({svc: time.time() - details["last_heartbeat"] for svc, details in services.items()})
    return {svc: details for svc, details in services.items() if time.time() - details["last_heartbeat"] < HEARTBEAT_EXPIRE}


def get_leader():
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    leader = redis_client.get(LEADER_KEY)
    instances = json.loads(redis_client.get(INSTANCE_INFO_KEY) or "{}")

    if leader and (leader in instances) and (time.time() - instances[leader]["last_heartbeat"] < HEARTBEAT_EXPIRE):
        leader_address = instances[leader]["address"]
    else:
        # leader is unavailable. we need to select a new one.
        available_executors = get_available_services(redis_client)
        if not available_executors:
            print("No available executors.")
            return

        leader_id, leader_info = random.choice(list(available_executors.items()))
        leader_address = leader_info["address"]
        print(f"New executor has been selected: {leader_id} with address: {leader_address}")

    return leader_address
# =============== temp ===============


def assign_order_id(order_details):
    order_details["orderId"] = str(uuid.uuid4())


def process_orders():
    leader_address = get_leader()

    try:
        channel = grpc.insecure_channel(leader_address)
        stub = order_executor_pb2_grpc.OrderExecutorServiceStub(channel)
        response = stub.ProcessOrder(order_executor_pb2.ProcessOrderRequest())
        print(f"Response from executor: {response.order_json}")
    except grpc.RpcError as e:
        print(f"Failed to process order with executor at {leader_address}: {e}")

    return {
        "success": response.success, 
        "order_json": json.loads(response.order_json),
        "order_result": json.loads(response.order_result)
    }



# @app.route('/checkout', methods=['POST'])
# def checkout():
#     order_details = request.json
#     print(order_details)
    
#     if not order_details:
#         return jsonify({'error': 'Invalid request'}), 400
    
    
#     enqueue_order(order_details)
#     results = process_orders()

#     print(results)
#     raise

#     if results["success"]:
#         return jsonify({
#             'orderId': results["order_json"].get('orderId', 'Unknown'),
#             'status': 'Order Approved',
#             'suggestedBooks': results["order_result"].get('suggested_books', [])
#         }), 200
#     else:
#         return 


@app.route('/checkout', methods=['POST', 'OPTIONS'])
def checkout():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200
    
    order_details = request.json
    print(order_details)
    
    if not order_details:
        return jsonify({'error': 'Invalid request'}), 400
    
    enqueue_order(order_details)
    results = process_orders()

    print(results)
    
    if results["success"]:
        return jsonify({
            'orderId': results["order_json"].get('orderId', 'Unknown'),
            'status': 'Order Approved',
            'suggestedBooks': results["order_result"].get('suggested_books', [])
        }), 200
    else:
        return jsonify({
            'orderId': results["order_json"].get('orderId', 'Unknown'),
            'status': 'Order Rejected',
            'suggestedBooks': results["order_result"].get('suggested_books', [])
        }), 200


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

