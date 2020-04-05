FROM python:3.7

USER root

WORKDIR /app

ADD dash /app

COPY dash/requirements.txt /
RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]
