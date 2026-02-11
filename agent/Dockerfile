FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
# Start the Streamlit UI in-container so docker-compose can expose it on 8501
# Note: build context for this Dockerfile is the agent/ directory, so the UI is at /app/ui/streamlit_app.py
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
