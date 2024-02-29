from pymongo import MongoClient

client = MongoClient('mongodb://admin:password@mongodb:27017')
db = client['bookstore']
books_collection = db['books']

books_data = [
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
]

books_collection.insert_many(books_data)
print("Books data has been inserted successfully.")
