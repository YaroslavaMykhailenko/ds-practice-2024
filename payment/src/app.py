import grpc
from concurrent import futures
import json

from utils.pb.payment import payment_pb2
from utils.pb.payment import payment_pb2_grpc

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    def __init__(self):
        self.running = False
        self.orders_cache = {}

    def lock_user_account(self, user_details):
        """
        In theory: Blocks the user's account to prevent other payments.
        In practice: Checks whether there are enough funds in the account and reserves the required amount for the transaction.
        Returns True if the account was successfully blocked.
        """
        # Let's imagine that here we are checking and blocking funds on the user's account
        return True

    def unlock_user_account(self, user_details):
        """
        In theory: Releases the user's account after a transaction is completed or cancelled.
        In practice: Cancels the reservation of funds or confirms the write-off.
        Returns True if the account was successfully unlocked.
        """
        # Let's imagine that this is releasing account resources
        return True

    def process_payment(self, order_details):
        """
        In theory: Performs the actual debiting of funds from a blocked account.
        In practice: Confirms the transaction and debits the money.
        Returns True if the payment was successful.
        """
        # Let's imagine that a payment is being made here
        return True

    def Prepare(self, request, context):
        try:
            if self.running:
                print('Payment system is busy now')
                return payment_pb2.PrepareResponse(willCommit=False, message="Prepare")
            
            order_details = json.loads(request.order_details_json)
            
            if self.lock_user_account(order_details['creditCard']):
                self.running = True
                self.orders_cache[request.order_id] = order_details
                print('Account was successfully blocked to prevent other payments.')

                return payment_pb2.PrepareResponse(willCommit=True, message="Prepare")
            else:
                print('Could not block user account')
                return payment_pb2.PrepareResponse(willCommit=False, message="Prepare")
        except grpc.RpcError:
            abort_book_response = self.Abort(payment_pb2.AbortRequest(order_id=request.order_id, message="Prepare"))
            if abort_book_response.success == False:
                return payment_pb2.PrepareResponse(willCommit=abort_book_response.success, message="Prepare")

    def Commit(self, request, context):
        if request.order_id in self.orders_cache:
            order_details = self.orders_cache.pop(request.order_id)
            try:
                self.process_payment(order_details)
                self.unlock_user_account(order_details['creditCard'])
                self.running = False
                print('Payment successful!')
                return payment_pb2.CommitResponse(success=True, message="Commit", order_details_json=json.dumps(order_details))
            except grpc.RpcError:
                return payment_pb2.CommitResponse(success=False, message="Commit", order_details_json=json.dumps(order_details))
        else:
            return payment_pb2.CommitResponse(success=False, message="Commit", order_details_json=json.dumps(order_details))

    def Abort(self, request, context):
        order_details = None
        if request.order_id in self.orders_cache:
            order_details = self.orders_cache.pop(request.order_id)
            self.unlock_user_account(order_details['creditCard'])

        self.running = False
        return payment_pb2.AbortResponse(success=False, message="Abort", 
                                         order_details_json=json.dumps(order_details) if order_details else {})

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    server.add_insecure_port('[::]:50058')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
