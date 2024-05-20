import grpc
from concurrent import futures
import os
import threading
import json
from kazoo.client import KazooClient
from pymongo import MongoClient
from utils.pb.book_storage import book_storage_pb2, book_storage_pb2_grpc



class BookStorage(book_storage_pb2_grpc.BookStorageServicer):
    def __init__(self, zk_hosts, node_id, mongo_uri):
        self.node_id = node_id
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()
        self.lock = threading.Lock()

        self.client = MongoClient(mongo_uri)
        self.db = self.client.bookstore
        self.books_collection = self.db.books

        self.objects = {}
        self.next_node = None
        self.prev_node = None
        self.head_stub = None
        self.tail_stub = None

        self.register_with_zookeeper()
        self.setup_chain()

        self.orders_cache = {}
        

    def register_with_zookeeper(self):
        self.zk.ensure_path("/chain")
        address = f"{self.node_id}:50060"
        path = f"/chain/{self.node_id}"
        if not self.zk.exists(path):
            self.zk.create(path, value=address.encode(), ephemeral=True, sequence=False)
            print(f"Registered {self.node_id} at {path} with address {address}")

    def setup_chain(self):
        if self.zk.exists("/chain"):
            self.zk.ChildrenWatch("/chain", self.handle_chain_update)

    def handle_chain_update(self, children):
        nodes = sorted(children)
        idx = nodes.index(self.node_id)
        self.prev_node = nodes[idx - 1] if idx > 0 else None
        self.next_node = nodes[idx + 1] if idx + 1 < len(nodes) else None
        self.update_stubs(nodes)

    def update_stubs(self, nodes):
        if nodes:
            head_data, _ = self.zk.get(f"/chain/{nodes[0]}")
            tail_data, _ = self.zk.get(f"/chain/{nodes[-1]}")
            self.head_stub = book_storage_pb2_grpc.BookStorageStub(grpc.insecure_channel(head_data.decode()))
            self.tail_stub = book_storage_pb2_grpc.BookStorageStub(grpc.insecure_channel(tail_data.decode()))
            self.is_head = self.node_id == nodes[0]
            self.is_tail = self.node_id == nodes[-1]
    
    def reconfigure_chain(self):
        try:
            if self.zk.exists("/chain"):
                nodes = sorted(self.zk.get_children("/chain"))
                idx = nodes.index(self.node_id)
                self.prev_node = nodes[idx - 1] if idx > 0 else None
                self.next_node = nodes[idx + 1] if idx + 1 < len(nodes) else None
                self.update_stubs(nodes)
                print(f"Chain reconfigured. Node {self.node_id} now has next: {self.next_node}, prev: {self.prev_node}")
                print()
        except Exception as e:
            print(f"Failed to reconfigure the chain due to: {e}")


    def Write(self, request, context):
        with self.lock:
            book = self.books_collection.find_one({"id": request.key})

            if 'versions' in book and book:
                new_version_number = book['versions'][-1]['version'] + 1
            else:
                new_version_number = 1
                
            new_version = {
                "version": new_version_number,
                "title": request.value.title,
                "author": request.value.author,
                "description": request.value.description,
                "copies": request.value.copies,
                "copiesAvailable": request.value.copiesAvailable,
                "category": request.value.category,
                "img": request.value.img,
                "price": request.value.price,
                "clean": False
            }

            if book:
                self.books_collection.update_one(
                    {"_id": book['_id']},
                    {"$set": {"versions": [new_version]}}
                    # {"$push": {"versions": new_version}}
                )
            else:
                self.books_collection.insert_one({
                    "id": request.key, 
                    "versions": [new_version]
                    })

            print(f"Updated MongoDB with key {request.key} to version {new_version_number}")


            print(f"=" * 25)
            print(f"[Write] - Node info...")
            print(f"=" * 25)

            print(f"-" * 25)
            print(f"node_id: {self.node_id}")
            print(f"is_head: {self.is_head}, is_tail: {self.is_tail}")
            print(f"prev_node: {self.prev_node}, next_node: {self.next_node}")
            print()
            print(f"versions: {new_version}")
            print(f"next_node: {self.next_node}")
            print(f"-" * 25)
            print()

            print(f"id: {request.key}, new_version_number: {new_version_number}")

            # 2.3.4  Chain Replication with Apportioned Queries
            # - When a node receives a new version of an object (via
            # a write being propagated down the chain), the node
            # appends this latest version to its list for the object
            if self.next_node:
                self.propagate_write(request)
            else:
                # this is tail - backprop.
                self.mark_version_as_clean(request.key, new_version_number)
                self.send_clean_ack(request.key, new_version_number)

            return book_storage_pb2.WriteResponse(success=True)


    def propagate_write(self, request):
        if self.next_node:

            print(f"=" * 25)
            print(f"[Write] - Calling next node...")
            print(f"=" * 25)

            print(f"-" * 25)
            print(f"node_id: {self.node_id}")
            print(f"is_head: {self.is_head}, is_tail: {self.is_tail}")
            print(f"prev_node: {self.prev_node}, next_node: {self.next_node}")
            print()
            print(f"calling next_node: {self.next_node} at: [{self.next_node}:50060]")
            print()

            try:
                with grpc.insecure_channel(f"{self.next_node}:50060") as channel:
                    stub = book_storage_pb2_grpc.BookStorageStub(channel)
                    stub.Write(book_storage_pb2.WriteRequest(key=request.key, value=request.value))
            except grpc.RpcError:
                print("[Write] - calling reconfigure_chain()...")
                raise
                self.reconfigure_chain()
                self.propagate_write(request) 


    def CleanVersion(self, request, context):
        # 2.3.3  Chain Replication with Apportioned Queries
        # When an acknowledgment message for an object version arrives at a node, 
        # the node marks the object version as clean. The node can then delete 
        # all prior versions of the object.
        self.mark_version_as_clean(request.key, request.version)
        self.send_clean_ack(request.key, request.version)

        return book_storage_pb2.CleanVersionResponse(success=True)


    def mark_version_as_clean(self, key, version):
        print(f"=" * 25)
        print(f"[Update] - Updating key state...")
        print(f"=" * 25)
        print(f"-" * 25)

        book = self.books_collection.find_one({"id": key})
        print(f"prev: {book['versions']}")
        
        # Update the document in MongoDB to mark the version as clean
        update_result = self.books_collection.update_one(
            {"id": key, "versions.version": version},
            {"$set": {"versions.$.clean": True}}
        )

        book = self.books_collection.find_one({"id": key})
        print(f"upd: {book['versions']}")

        if update_result.modified_count == 1:
            print(f"Successfully marked version {version} of key {key} as clean.")
        else:
            print(f"Failed to mark version {version} of key {key} as clean. Document might not exist or version number mismatch.")

        print()


    def send_clean_ack(self, key, version):
        if self.prev_node:
            print(f"=" * 25)
            print(f"[Clean] - Chain back traversal...")
            print(f"=" * 25)
            print(f"-" * 25)
            print(f"(key, version): ({key}, {version})")
            print(f"node_id: {self.node_id}")
            print(f"prev_node: {self.prev_node}")
            print(f"-" * 25)
            print()

            try:
                with grpc.insecure_channel(f"{self.prev_node}:50060") as channel:
                    stub = book_storage_pb2_grpc.BookStorageStub(channel)
                    stub.CleanVersion(book_storage_pb2.CleanVersionRequest(key=key, version=version))
            except grpc.RpcError as e:
                print(f"Failed to send clean ack to {self.prev_node}. Error: {e}")


    def Read(self, request, context):
        with self.lock:
            book = self.books_collection.find_one({"id": request.key}, {"versions": {"$slice": -1}})

            print(f"=" * 25)
            print(f"[Read] - Node info...")
            print(f"=" * 25)

            print(f"-" * 25)
            print(f"node_id: {self.node_id}")
            print(f"is_head: {self.is_head}, is_tail: {self.is_tail}")
            print(f"prev_node: {self.prev_node}, next_node: {self.next_node}")
            print()
            print(f"book: {book}")
            print(f"next_node: {self.next_node}")
            print(f"-" * 25)
            print()

            if book:
                latest_version = book['versions'][-1]

                book_info = book_storage_pb2.Book(
                    id=book['id'],
                    title=latest_version['title'],
                    author=latest_version['author'],
                    description=latest_version['description'],
                    copies=latest_version['copies'],
                    copiesAvailable=latest_version['copiesAvailable'],
                    category=latest_version['category'],
                    img=latest_version['img'],
                    price=latest_version['price']
                )
                
                # 2.3.4  Chain Replication with Apportioned Queries
                # - When a node receives a read request for an object
                if latest_version['clean']:
                    return book_storage_pb2.ReadResponse(value=book_info, 
                                                         clean=latest_version['clean'], 
                                                         found=True)
                else:
                    print(f"[Read] - Querying tail from {self.node_id}")
                    print()

                    clean_response = self.query_tail_for_clean_version(request.key)
                    if clean_response.found:
                        self.mark_version_as_clean(request.key, latest_version['version'])

                        return book_storage_pb2.ReadResponse(value=clean_response.value, 
                                                             clean=latest_version['clean'], 
                                                             found=True)
                    else: 
                        latest_clean_version = None
                        for version in reversed(book['versions']):
                            if version['clean']:
                                latest_clean_version = version
                                break   
                        
                        if latest_clean_version:
                            return book_storage_pb2.ReadResponse(value=book_info, 
                                                                 clean=latest_clean_version['clean'], 
                                                                 found=True)


            return book_storage_pb2.ReadResponse(found=False)


    def query_tail_for_clean_version(self, key):
        try:
            response = self.tail_stub.Read(book_storage_pb2.ReadRequest(key=key))
            return response
        except grpc.RpcError as e:
            print(f"Failed to fetch clean version from tail. Error: {e}")
            return book_storage_pb2.ReadResponse(found=False)


    def DecrementStock(self, request, context=None):
        # with self.lock:
        book = self.books_collection.find_one({"id": request.key})
        
        if book:
            latest_version = book['versions'][-1]

            new_version = dict(latest_version)
            new_version['copiesAvailable'] -= request.value
            new_version['version'] += 1
            new_version['clean'] = False

            self.books_collection.update_one(
                {"_id": book['_id']},
                {"$set": {"versions": [new_version]}}
                # {"$push": {"versions": new_version}}
            )

            book = book_storage_pb2.Book(
                id=request.key,
                title=new_version['title'],
                author=new_version['author'],
                description=new_version['description'],
                copies=new_version['copies'],
                copiesAvailable=new_version['copiesAvailable'],
                category=new_version['category'],
                img=new_version['img'],
                price=new_version['price']
            )

            self.propagate_write(book_storage_pb2.WriteRequest(key=request.key, value=book))
            return book_storage_pb2.StockUpdateResponse(success=True)
        
        return book_storage_pb2.StockUpdateResponse(success=False)
        

    def IncrementStock(self, request, context=None):
        # with self.lock:
        book = self.books_collection.find_one({"id": request.key})
        
        if book:
            latest_version = book['versions'][-1]

            new_version = dict(latest_version)
            new_version['copiesAvailable'] += request.value
            new_version['version'] += 1
            new_version['clean'] = False

            self.books_collection.update_one(
                {"_id": book['_id']},
                {"$set": {"versions": [new_version]}}
                # {"$push": {"versions": new_version}}
            )

            book = book_storage_pb2.Book(
                id=request.key,
                title=new_version['title'],
                author=new_version['author'],
                description=new_version['description'],
                copies=new_version['copies'],
                copiesAvailable=new_version['copiesAvailable'],
                category=new_version['category'],
                img=new_version['img'],
                price=new_version['price']
            )

            self.propagate_write(book_storage_pb2.WriteRequest(key=request.key, value=book))
            return book_storage_pb2.StockUpdateResponse(success=True)
        
        return book_storage_pb2.StockUpdateResponse(success=False)


    def CheckStock(self, request, context=None):
        book = self.books_collection.find_one({"id": request.key}, {"versions": {"$slice": -1}})
        if book:
            latest_version = book['versions'][0]
            return book_storage_pb2.CheckStockResponse(
                copiesAvailable=latest_version['copiesAvailable'],
                success=True
            )
        return book_storage_pb2.CheckStockResponse(success=False, message="Book not found.")


    def Prepare(self, request, context):
        order_details = json.loads(request.order_details_json)
        order_id = request.order_id

        with self.lock:
            try:
                print(f"=" * 25)
                print(f"[Prepare] - Node info...")
                print(f"=" * 25)

                print(f"-" * 25)
                print(f"node_id: {self.node_id}")
                print()

                for item in order_details['items']:
                    book_id = item['id']
                    print(f"book_id: {book_id}")
                    required_quantity = item['quantity']
                    book = self.books_collection.find_one({"id": book_id})
                    
                    print(f"book: {book}")

                    # copiesAvailable = self.CheckStock(book_storage_pb2.CheckStockRequest(key=book_id))
                    copiesAvailable = book['versions'][-1]['copiesAvailable']
                    is_reserved = book.get('reserved', False)

                    print(f"copiesAvailable: {copiesAvailable}")

                    if book and copiesAvailable >= required_quantity: #and not is_reserved:
                        self.books_collection.update_one(
                            {"id": book_id},
                            {"$set": {"reserved": True}}
                        )
                    else:
                        return book_storage_pb2.PrepareResponse(willCommit=False, message="Prepare")

                self.orders_cache[order_id] = order_details


                
                print()
                print(f'book: {self.books_collection.find_one({"id": book_id})}')
                print()
                print(f"orders_cache: {self.orders_cache}")
                print(f"-" * 25)
                print()

                
                return book_storage_pb2.PrepareResponse(willCommit=True, message="Prepare")
            except Exception as e:
                self.Abort(book_storage_pb2.AbortRequest(order_id=order_id))
                return book_storage_pb2.PrepareResponse(willCommit=False, message="Prepare")


    def Commit(self, request, context):
        order_id = request.order_id

        with self.lock:
            if order_id in self.orders_cache:
                order_details = self.orders_cache.pop(order_id)

                try:
                    for item in order_details['items']:
                        book_id = item['id']
                        quantity = item['quantity']

                        print(f"=" * 25)
                        print(f"[Commit] - Node info...")
                        print(f"=" * 25)
                        print(f"-" * 25)
                        print(f"node_id: {self.node_id}")
                        print(f"-" * 25)
                        print("Decrement:")
                        print(f"-" * 25)
                        print(f"book_id: {book_id}, quantity: {quantity}")
                        _prev_book = self.books_collection.find_one({"id": book_id})
                        print(f"-" * 25)

                        self.DecrementStock(book_storage_pb2.StockUpdateRequest(key=book_id, value=quantity))

                        self.books_collection.update_one(
                            {"id": book_id},
                            {"$set": {"reserved": False}}
                        )

                        print()
                        print(f'prev book: {_prev_book}')
                        print()
                        print(f'dec book: {self.books_collection.find_one({"id": book_id})}')
                        print(f"orders_cache: {self.orders_cache}")
                        print(f"-" * 25)
                        print()
                        
                    return book_storage_pb2.CommitResponse(success=True, message="Commit")
                except Exception as e:
                    print(e)
                    return book_storage_pb2.CommitResponse(success=False, message="Commit")
            else:
                return book_storage_pb2.CommitResponse(success=False, message="Commit")


    def Abort(self, request, context):
        order_id = request.order_id

        with self.lock:
            if order_id in self.orders_cache:
                order_details = self.orders_cache.pop(order_id)

                for item in order_details['items']:
                    book_id = item['id']
                    self.books_collection.update_one(
                        {"id": book_id},
                        {"$set": {"reserved": False}}
                    )

                print(f"=" * 25)
                print(f"[Abort] - Node info...")
                print(f"=" * 25)

                print(f"-" * 25)
                print(f"node_id: {self.node_id}")
                print()
                print(f'book: {self.books_collection.find_one({"id": book_id})}')
                print(f"orders_cache: {self.orders_cache}")
                print(f"-" * 25)
                print()

                return book_storage_pb2.AbortResponse(success=False, message="Abort")
            return book_storage_pb2.AbortResponse(success=True, message="Abort")


 


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = BookStorage(os.getenv("ZK_HOSTS"), os.getenv("SERVICE_ID"), os.getenv("MONGO_URI"))
    book_storage_pb2_grpc.add_BookStorageServicer_to_server(service, server)
    server.add_insecure_port('[::]:50060')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


