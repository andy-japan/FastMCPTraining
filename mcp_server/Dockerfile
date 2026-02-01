FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["fastmcp", "run", "main.py", "--transport", "sse", "--port", "8000", "--host", "0.0.0.0"]
