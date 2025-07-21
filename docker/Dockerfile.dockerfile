FROM ubuntu:latest

LABEL version="1.0"
LABEL description="テスト"
RUN apt-get update && apt install -y apache2
RUN apt-get update && apt install -y git