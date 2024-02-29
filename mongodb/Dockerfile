FROM mongo

# Install Python and Pip
# RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY mongodb/init_books.py /docker-entrypoint-initdb.d/init_books.py

# Install any Python dependencies
# RUN pip3 install pymongo

# MongoDB will execute scripts in docker-entrypoint-initdb.d on startup
