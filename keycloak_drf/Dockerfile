FROM python:3.8

# set work directory
WORKDIR /keycloak_dr

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY . .

RUN pip install -r requirments.py