FROM alpine:latest

# # # RUN apk add --no-cache python3-dev \
# # #     && pip3 install --upgrade pip
RUN apk add --no-cache --update python3 py3-pip python3-dev \
    && pip3 install --upgrade pip

# ADD repositories /etc/apk/repositories
# RUN apk add --update python python-dev gfortran py-pip build-base py-numpy@community
# FROM python:3.6-alpine3.7

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev
    
RUN pip install --upgrade cython

# RUN pip install numpy


# # RUN pip install numpy
# RUN pip install pandas
# RUN pip install scikit-learn
# RUN pip install scipy
# # RUN pip install setuptools
# # RUN pip install scipy
# RUN pip install sklearn
# RUN pip install flask
# RUN pip install pickle-mixin
# RUN pip install bson



WORKDIR /app 

COPY . /app

ADD requirements.txt .
RUN pip  install -r requirements.txt
