FROM python:3.11-alpine
LABEL authors="mao1313"

WORKDIR app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .


CMD ["python", "main.py"]