import grpc
import json
import sys
sys.path.append("./")

from utils.pb.book_storage import book_storage_pb2, book_storage_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:50060') as channel:
        stub = book_storage_pb2_grpc.BookStorageStub(channel)
        
        
        # Create a new book entry
        new_book = book_storage_pb2.Book(
            id="5",
            title="React - Up & Running",
            author="Carlos Stevens",
            description="Building Web Applications with React.",
            copies=10,
            copiesAvailable=10,
            category="Web Development",
            img="https://m.media-amazon.com/images/I/418mC3XLQlL._SY445_SX342_.jpg",
            price=12
        )

        write_response = stub.Write(book_storage_pb2.WriteRequest(key="5", value=new_book))
        print(f"Write Response: {write_response.success}")

        order_json = json.dumps({
            "user": {"name": "Yaroslava", "contact": "58180469"},
            "creditCard": {"number": "1234567890987654", "expirationDate": "12/26", "cvv": "123"},
            "userComment": "",
            "items": [{
                "id": "10",
                "title": "Advanced CSS and Sass",
                "author": "Alex Johnson",
                "description": "Take your CSS to the next level with Sass.",
                "copies": 8,
                "copiesAvailable": 8,
                "category": "Web Design",
                "img": "https://m.media-amazon.com/images/I/51CsK0NNtxL._SY445_SX342_.jpg",
                "price": 12,
                "quantity": 1
            }],
            "discountCode": "",
            "shippingMethod": "",
            "giftMessage": "",
            "billingAddress": {
                "street": "turu 7",
                "city": "tartu",
                "state": "Estonia",
                "zip": "51004",
                "country": "Estonia"
            },
            "giftWrapping": False,
            "termsAndConditionsAccepted": True,
            "notificationPreferences": ["email"],
            "device": {
                "type": "Smartphone",
                "model": "Samsung Galaxy S10",
                "os": "Android 10.0.0"
            },
            "browser": {
                "name": "Chrome",
                "version": "85.0.4183.127"
            },
            "appVersion": "3.0.0",
            "screenResolution": "1440x3040",
            "referrer": "https://www.google.com",
            "deviceLanguage": "en-US",
            "orderId": "31df022a-295c-46e5-a6ef-df6074f1d014"
        })

        prepare_response = stub.Prepare(book_storage_pb2.PrepareRequest(order_id="31df022a-295c-46e5-a6ef-df6074f1d014", order_details_json=order_json))
        print(f"Prepare Response: {prepare_response.willCommit}, Message: {prepare_response.message}")

        if prepare_response.willCommit:
            commit_response = stub.Commit(book_storage_pb2.CommitRequest(order_id="31df022a-295c-46e5-a6ef-df6074f1d014"))
            print(f"Commit Response: {commit_response.success}, Message: {commit_response.message}")

if __name__ == "__main__":
    main()
