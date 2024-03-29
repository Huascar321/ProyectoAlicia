FROM ubuntu:20.04
FROM python:3.6-stretch
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==1.10.2 && pip install pandas
ADD . /app/
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh
