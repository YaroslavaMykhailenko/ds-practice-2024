from utils.pb.fraud_detection import fraud_detection_pb2, fraud_detection_pb2_grpc
from utils.pb.transaction_verification import transaction_verification_pb2, transaction_verification_pb2_grpc
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc
from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.pb.order_executor import order_executor_pb2, order_executor_pb2_grpc


# from opentelemetry import metrics
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View


from opentelemetry import trace, metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View




import time

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
logger.info(f"initializing orchestrator with MONGO_URI: {MONGO_URI}")
client = MongoClient(MONGO_URI)
db = client['bookstore']

# resource = Resource(attributes={
#     SERVICE_NAME: "orchestrator"
# })
trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "orchestrator"})))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://observability:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Flask, gRPC and Redis
FlaskInstrumentor().instrument_app(app)
GrpcInstrumentorClient().instrument()
RedisInstrumentor().instrument()


reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4317")
)

duration_histogram_view = View(
    instrument_type=metrics.Histogram,
    aggregation=ExplicitBucketHistogramAggregation(
        boundaries=[10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000]
    )
)



meterProvider = MeterProvider(
    resource=Resource.create({SERVICE_NAME: "orchestrator"}),
    metric_readers=[reader],
    views=[duration_histogram_view]
)

metrics.set_meter_provider(meterProvider)

order_approved_counter = meterProvider.get_meter(__name__).create_counter(
    "orchestrator_order_approved_count",
    description="Counts the number of approved orders",
    unit="1",
)

order_rejected_counter = meterProvider.get_meter(__name__).create_counter(
    "orchestrator_order_rejected_count",
    description="Counts the number of rejected orders",
    unit="1",
)

duration_histogram = meterProvider.get_meter(__name__).create_histogram(
    "orchestrator_duration_ms",
    description="Duration distribution of orchestrator requests in milliseconds",
    unit="milliseconds",
)



# TODO: these functions should be outside
# @app.route('/api/books', methods=['GET'])
# def get_books():
#     books_cursor = db.books.find({})
#     books = list(books_cursor)
#     # print(books)
#     for book in books:
#         book['_id'] = str(book['_id'])

#     if books:
#         return jsonify(books)
#     else:
#         return jsonify({"error": "Books not found"}), 404


# @app.route('/api/books/<bookId>', methods=['GET'])
# def get_book(bookId):
#     book = db.books.find_one({"id": bookId}, {'_id': 0})
#     print(book)
#     if book:
#         return jsonify(book)
#     else:
#         return jsonify({"error": "Book not found"}), 404



@app.route('/api/books', methods=['GET'])
def get_books():

    books_cursor = db.books.find({})
    books = list(books_cursor)
    for book in books:
        book['_id'] = str(book['_id'])
        if 'versions' in book and book['versions']:
            latest_version = book['versions'][-1]
            for key, value in latest_version.items():
                book[key] = value
            del book['versions']

    if books:
        return jsonify(books)
    else:
        return jsonify({"error": "Books not found"}), 404


@app.route('/api/books/<bookId>', methods=['GET'])
def get_book(bookId):
    book = db.books.find_one({"id": bookId}, {'_id': 0})
    if book:
        if 'versions' in book and book['versions']:
            latest_version = book['versions'][-1]
            for key, value in latest_version.items():
                book[key] = value
            del book['versions']
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
        # print(f"Response from executor: {response.order_json}")
    except grpc.RpcError as e:
        print(f"Failed to process order with executor at {leader_address}: {e}")

    return {
        "success": response.success, 
        "order_json": json.loads(response.order_json),
        "order_result": json.loads(response.order_result)
    }


def confirm_order(results):
    return results.get("success", False) \
        and not results["order_result"].get("is_fraudulent", True) \
        and results["order_result"].get("is_valid", False)



@app.route('/checkout', methods=['POST', 'OPTIONS'])
def checkout():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("checkout"):
        start_time = time.time()

        if request.method == 'OPTIONS':
            return jsonify({'status': 'OK'}), 200
        
        order_details = request.json
        print("order_details")
        print(order_details)
        
        if not order_details:
            return jsonify({'error': 'Invalid request'}), 400
        
        with tracer.start_as_current_span("enqueue_order"):
            enqueue_order(order_details)

        with tracer.start_as_current_span("process_orders"):
            results = process_orders()

        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000  # Convert duration to milliseconds
        duration_histogram.record(duration_ms)


        print("results")
        print(results)
        
        # if confirm_order(results):
        if results["success"]:
            order_approved_counter.add(1, {"service": "orchestrator", "status": "Order Approved"})
            return jsonify({
                'orderId': results["order_json"].get('orderId', 'Unknown'),
                'status': 'Order Approved',
                'suggestedBooks': results["order_result"].get('suggested_books', [])
            }), 200
        else:
            order_rejected_counter.add(1, {"service": "orchestrator", "status": "Order Rejected"})
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

