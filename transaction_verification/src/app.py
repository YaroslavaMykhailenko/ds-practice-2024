import grpc
from concurrent import futures
import json
import re

from utils.pb.transaction_verification import transaction_verification_pb2
from utils.pb.transaction_verification import transaction_verification_pb2_grpc

from tools.logging import setup_logger
logger = setup_logger("transaction_verification")


class TransactionVerificationService(transaction_verification_pb2_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        order = json.loads(request.order_json)

        # if not self.user_info_valid(order.get('user', {})):
        #     return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False)
        
        # if not self.payment_details_valid(order.get('creditCard', {})):
        #     return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False)
        
        # if not self.billing_address_valid(order.get('billingAddress', {})):
        #     return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False)
        
        # if not self.check_items_availability(order.get('items', [])):
        #     return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False)

        return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True)
        

    # Check if the user information is not empty  
    def user_info_valid(self, user):

        name = user.get('name')
        contact = user.get('contact')
        
        if not name or not contact:
            return False
        
        if not re.match('^\+?\d{7,15}$', contact):
            return False
        
        return True

    
    # Check if the paiment info is not empty and valid  
    def payment_details_valid(self, credit_card):

        card_number = credit_card.get('number', '')
        expiration_date = credit_card.get('expirationDate', '')
        cvv = credit_card.get('cvv', '')        
        
        if not card_number or not cvv or not expiration_date:
            return False
        if not re.match(r"^\d{13,19}$", card_number) or not self.passes_luhn_check(card_number):
            return False
        if not re.match(r"^\d{3,4}$", cvv):
            return False
        if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiration_date):
            return False
        
        return True
    
    # Check if the billing adress info is not empty
    def billing_address_valid(self, billing_address):
        fields = ['street', 'city', 'state', 'zip', 'country']
        for field in fields:
            if not billing_address.get(field):
                return False
        return True
    
    def check_items_availability(self, items):
        return isinstance(items, list) and len(items) > 0

    
    # Luhn algorithm to check the card number's validity.
    def passes_luhn_check(self, card_number):
        total = 0
        num_digits = len(card_number)
        odd_even = num_digits & 1
        
        for count in range(num_digits):
            digit = int(card_number[count])
            
            if not ((count & 1) ^ odd_even):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            
            total += digit
        
        return (total % 10) == 0


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServiceServicer_to_server(TransactionVerificationService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()