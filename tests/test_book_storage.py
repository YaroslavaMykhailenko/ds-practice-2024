# import grpc

# import sys
# sys.path.append("./")

# from utils.pb.book_storage import book_storage_pb2, book_storage_pb2_grpc


# channel = grpc.insecure_channel('localhost:50060')
# stub = book_storage_pb2_grpc.BookStorageStub(channel)

# write_response = stub.Write(book_storage_pb2.WriteRequest(key="003", value="New Title: New Book"))
# read_response = stub.Read(book_storage_pb2.ReadRequest(key="003"))

# print(read_response)



import grpc
import sys
sys.path.append("./")  # Assuming your protobuf files are compiled in a visible directory.

from utils.pb.book_storage import book_storage_pb2, book_storage_pb2_grpc

def main():
    # Setup the gRPC channel and stub
    with grpc.insecure_channel(f"localhost:50060") as channel:
        stub = book_storage_pb2_grpc.BookStorageStub(channel)

        # Create a new book entry
        new_book = book_storage_pb2.Book(
            id="9",
            title="Effective Python",
            author="Brett Slatkin",
            description="59 Specific Ways to Write Better Python",
            copies=5,
            copiesAvailable=5,
            category="Programming",
            img="https://example.com/effective_python.jpg",
            price=30
        )

        # Write the new book to the database
        write_response = stub.Write(book_storage_pb2.WriteRequest(key="9", value=new_book))
        print(f"Write Response: {write_response.success}")

        # Read the book back from the database
        read_response = stub.Read(book_storage_pb2.ReadRequest(key="9"))
        if read_response.found:
            print(f"Read Response: {read_response.value}")
        else:
            print("Book not found.")

if __name__ == "__main__":
    main()
