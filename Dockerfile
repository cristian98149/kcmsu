FROM python:3.11-slim

WORKDIR /app
COPY ./src /app

RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Define the command to run your app (this example uses Flask)
CMD ["python", "main.py"]
