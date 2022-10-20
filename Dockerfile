FROM python:3.6-jessie
RUN apt update
WORKDIR /app
ADD . /app
RUN pip install -r /app/requirements.txt

CMD ["gunicorn", "app:app", "--config=config.py"]