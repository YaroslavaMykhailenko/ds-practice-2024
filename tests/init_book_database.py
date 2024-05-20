# NOTE: this needs to be run only one time for new docker containers

import grpc
import sys
import json
sys.path.append("./")

from utils.pb.book_storage import book_storage_pb2, book_storage_pb2_grpc

def main():
    with grpc.insecure_channel(f"localhost:50060") as channel:
        stub = book_storage_pb2_grpc.BookStorageStub(channel)

        books = [
            {
                "id": "1",
                "title": "Learning Python",
                "author": "John Smith",
                "description": "An in-depth guide to Python programming.",
                "copies": 10,
                "copiesAvailable": 7,
                "category": "Programming",
                "img": "https://m.media-amazon.com/images/W/MEDIAX_792452-T1/images/I/51FD3C3kLiL.jpg",
                "price": 10
            },
            {
                "id": "2",
                "title": "JavaScript - The Good Parts",
                "author": "Jane Doe",
                "description": "Unearthing the excellence in JavaScript.",
                "copies": 15,
                "copiesAvailable": 15,
                "category": "Web Development",
                "img": "https://m.media-amazon.com/images/W/MEDIAX_792452-T1/images/I/91YlBt-bCHL._SL1500_.jpg",
                "price": 3
            },
            {
                "id": "3",
                "title": "Advanced CSS and Sass",
                "author": "Alex Johnson",
                "description": "Take your CSS to the next level with Sass.",
                "copies": 8,
                "copiesAvailable": 8,
                "category": "Web Design",
                "img": "https://m.media-amazon.com/images/I/51CsK0NNtxL._SY445_SX342_.jpg",
                "price": 12
            },
            {
                "id": "4",
                "title": "Data Structures and Algorithms",
                "author": "Emily White",
                "description": "Essential algorithms and data structures for optimal coding.",
                "copies": 12,
                "copiesAvailable": 11,
                "category": "Computer Science",
                "img": "https://m.media-amazon.com/images/I/61Mw06x2XcL._SY522_.jpg",
                "price": 20
            },
            {
                "id": "5",
                "title": "React - Up & Running",
                "author": "Carlos Stevens",
                "description": "Building Web Applications with React.",
                "copies": 10,
                "copiesAvailable": 10,
                "category": "Web Development",
                "img": "https://m.media-amazon.com/images/I/418mC3XLQlL._SY445_SX342_.jpg",
                "price": 5
            },
            {
                "id": "6",
                "title": "Machine Learning Yearning",
                "author": "Sophia Li",
                "description": "Techniques for effectively deploying machine learning applications.",
                "copies": 20,
                "copiesAvailable": 20,
                "category": "Machine Learning",
                "img": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1480798569i/30741739.jpg",
                "price": 18
            },
            {
                "id": "7",
                "title": "Cloud Computing Basics",
                "author": "David Miller",
                "description": "A beginner's guide to the world of cloud computing.",
                "copies": 7,
                "copiesAvailable": 6,
                "category": "Cloud Computing",
                "img": "https://m.media-amazon.com/images/I/41pzWJzPA3L._SY445_SX342_.jpg",
                "price": 9
            }
        ]

        for book in books:
            new_book = book_storage_pb2.Book(
                id=book["id"],
                title=book["title"],
                author=book["author"],
                description=book["description"],
                copies=book["copies"],
                copiesAvailable=book["copiesAvailable"],
                category=book["category"],
                img=book["img"],
                price=book["price"]
            )

            write_response = stub.Write(book_storage_pb2.WriteRequest(key=book["id"], value=new_book))
            print(f"Write Response for book ID {book['id']}: {write_response.success}")

            read_response = stub.Read(book_storage_pb2.ReadRequest(key=book["id"]))
            if read_response.found:
                print(f"Read Response for book ID {book['id']}: {read_response.value}")
            else:
                print(f"Book ID {book['id']} not found.")

if __name__ == "__main__":
    main()
