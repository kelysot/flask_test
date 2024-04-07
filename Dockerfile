FROM python:3.9-slim
WORKDIR /app/
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc python3-dev
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 5555
CMD ["python3", "app.py"]