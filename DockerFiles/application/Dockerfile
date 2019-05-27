FROM ubuntu:latest

MAINTAINER Suraj Nair "suraj.nair2410@gmail.com"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev build-essential libmysqlclient-dev

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]
