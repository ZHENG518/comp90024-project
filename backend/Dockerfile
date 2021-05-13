FROM python:3.7

RUN apt-get update && apt-get upgrade -y && apt-get install vim -y

RUN mkdir /root/backend
WORKDIR /root/backend

COPY . /root/backend/
RUN pip install -r /root/backend/requirement.txt

ENTRYPOINT ["python", "/root/backend/app.py"]