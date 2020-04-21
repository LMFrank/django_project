FROM python:3.8.2

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
COPY requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple