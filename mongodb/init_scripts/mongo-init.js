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
]);
