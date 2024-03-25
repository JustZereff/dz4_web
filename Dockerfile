FROM python:3.11.6-alpine

WORKDIR /app

COPY . .

EXPOSE 3000

CMD ["python", "main.py"]