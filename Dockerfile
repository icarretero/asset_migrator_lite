FROM python:3.8-slim

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
    libmariadbclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
