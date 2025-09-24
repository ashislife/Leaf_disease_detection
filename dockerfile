FROM python:3.10-slim
WORKDIR /app

# Model copy karo
COPY saved_models/ ./saved_models/

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "port", "8000"]