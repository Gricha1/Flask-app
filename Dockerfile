FROM python:3.8-slim-buster

WORKDIR /app


COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*



RUN pip install mysqlclient
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
