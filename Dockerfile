# ====================================================================== #
# Playstore Autoscale Docker Image
# ====================================================================== #

# Base image
# ---------------------------------------------------------------------- #
FROM python:3

# Author
# ---------------------------------------------------------------------- #
LABEL maintainer "kemuri@kemuri.de"

WORKDIR /usr/src/app

COPY requirements.txt ./

COPY google-play-service.json ./

RUN pip install --no-cache-dir -r requirements.txt

COPY playstore-autoscale.py ./

ENV GOOGLE_APPLICATION_CREDENTIALS=./google-play-service.json

CMD [ "python" , "./playstore-autoscale.py" ]
