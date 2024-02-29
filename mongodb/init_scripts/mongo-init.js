db.createUser({
  user: 'admin',
  pwd: 'password',
  roles: [
    {
      role: 'readWrite',
      db: 'bookstore',
    },
  ],
});


db.createCollection('books');

db.books.insertMany([
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
    "title": "Learning Python",
    "author": "John Smith",
    "description": "An in-depth guide to Python programming.",
    "copies": 10,
    "copiesAvailable": 7,
    "category": "Programming",
    "img": "https://m.media-amazon.com/images/W/MEDIAX_792452-T1/images/I/51FD3C3kLiL.jpg",
    "price": 10
  }, 
]);
