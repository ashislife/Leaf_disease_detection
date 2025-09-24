FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Correct path batao
CMD ["uvicorn", "Tamato_disease.api.main:app", "--host", "0.0.0.0", "--port", "8000"]