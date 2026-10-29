FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY expense_api.py .
ENV EXPENSE_DB=/data/expenses.db
RUN useradd --create-home appuser && mkdir /data && chown appuser /data
USER appuser
EXPOSE 8000
CMD ["uvicorn", "expense_api:app", "--host", "0.0.0.0", "--port", "8000"]
