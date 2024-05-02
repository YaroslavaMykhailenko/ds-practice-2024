FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . .
RUN cd utils/pb && pip install .
WORKDIR /app

COPY ./book_storage/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install reloadium

CMD reloadium run "book_storage/src/app.py"