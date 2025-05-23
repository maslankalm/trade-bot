FROM python:3.13-alpine
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "/app/trade.py"]
