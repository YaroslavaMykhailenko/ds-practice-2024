#!/bin/bash

# Start MongoDB container
docker-compose up -d mongodb

# Wait for MongoDB to be fully up
echo "Waiting for MongoDB to start..."
sleep 10  # Adjust sleep time as needed

# Run the Python script to initialize the database
python3 ./mongodb/init_books.py

echo "MongoDB has been initialized with books data."
