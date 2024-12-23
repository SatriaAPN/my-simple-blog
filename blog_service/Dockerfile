FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN chmod +x entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

COPY entrypoint.sh /app/entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]
