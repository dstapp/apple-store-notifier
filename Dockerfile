FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY notify.py ./
RUN chmod 777 /tmp

CMD [ "python", "./notify.py" ]
