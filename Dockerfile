FROM ubuntu:22.04

RUN apt-get install -y python3

RUN apt-get update

# RUN dependencias

CMD ["sh", "-c", "./start.sh"]
