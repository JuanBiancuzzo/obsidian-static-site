FROM node:20-slim as builder

WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json* .

RUN npm ci

# FROM node:20-slim
FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash

RUN apt-get install -y nodejs

RUN apt-get install -y pdf2svg

RUN apt-get install -y texlive-latex-base
RUN apt-get install -y --no-install-recommends texlive-latex-extra
# RUN apt-get install -y --no-install-recommends texlive-fonts-recommended texlive-fonts-extra
# RUN apt-get install -y --no-install-recommends texlive-fonts-extra-links

RUN apt-get install python3

# RUN fc-cache -f -v

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/ /usr/src/app/
COPY . .

CMD ["sh", "-c", "./start.sh"]
