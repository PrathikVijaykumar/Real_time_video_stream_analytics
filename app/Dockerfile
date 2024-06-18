FROM python:3.9-slim-buster

RUN apt-get -y update
RUN apt-get install -y ffmpeg

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501
EXPOSE 5003

CMD ["bash", "run.sh"]
