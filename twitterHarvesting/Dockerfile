FROM python:3.7

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV HTTP_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV no_proxy localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.u nimelb.edu.au,.cloud.unimelb.edu.au

RUN apt-get update && apt-get upgrade -y && apt-get install vim -y

RUN mkdir /root/twitterHarvesting
WORKDIR /root/twitterHarvesting

COPY . /root/twitterHarvesting/
RUN pip install -r /root/twitterHarvesting/requirement.txt

ENV DATABASE_IP localhost


ENTRYPOINT ["python", "/root/twitterHarvesting/src/harvest.py"]