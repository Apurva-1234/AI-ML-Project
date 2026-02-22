FROM python:3.10

WORKDIR /app
COPY backend/ backend/
COPY model/ model/

RUN pip install -r backend/requirements.txt

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
