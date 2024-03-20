FROM node:20-slim as builder

WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json .

RUN npm install -g npm@10.5.0
RUN npm ci

FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash

RUN apt-get install -y nodejs

RUN apt-get install -y pdf2svg

RUN apt-get install -y texlive-latex-base
RUN apt-get install -y --no-install-recommends texlive-latex-extra

RUN apt-get install python3 python3-pip
RUN pip install python-frontmatter

RUN apt-get install -y wget gnupg ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN which google-chrome-stable

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/ /usr/src/app/
COPY . .

CMD ["sh", "-c", "./start.sh"]
