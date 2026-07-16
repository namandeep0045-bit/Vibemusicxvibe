FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt update && apt install -y ffmpeg

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
