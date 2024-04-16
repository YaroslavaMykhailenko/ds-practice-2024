from concurrent import futures
import grpc
import json
import queue

from utils.pb.order_queue import order_queue_pb2
from utils.pb.order_queue import order_queue_pb2_grpc


class OrderQueueService(order_queue_pb2_grpc.OrderQueueServiceServicer):
    def __init__(self):
        self.order_queue = queue.PriorityQueue()
        
    def Enqueue(self, request, context):
        priority = request.priority
        order_json = request.order_json
        order_id = json.loads(order_json)["orderId"]

        with self.order_queue.mutex:
            self.order_queue.queue.clear()

        print(self.order_queue.queue)

        # print(f"order_id: {order_id}")
        # print(f"total_price: {priority}")
        # print(f"order_json: {order_json}")

        # min-heap.
        self.order_queue.put((-priority, order_id, order_json))
        return order_queue_pb2.EnqueueResponse(success=True)


    def Dequeue(self, request, context):
        if self.order_queue.empty():
            return order_queue_pb2.Order()
        
        _, order_id, order_json = self.order_queue.get()  # Adjusted to unpack three values
        return order_queue_pb2.Order(id=order_id, order_json=order_json, priority=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_pb2_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
