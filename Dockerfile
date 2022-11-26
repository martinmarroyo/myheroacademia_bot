FROM python:3.10-slim-bullseye
WORKDIR /mhabot
COPY utils ./utils
COPY Dockerfile main.py README.md requirements.txt ./
RUN pip install -r requirements.txt
CMD python -m main
