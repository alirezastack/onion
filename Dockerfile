FROM python:3.6-alpine
MAINTAINER Sayyed Alireza Hoseini <alireza.hosseini@zoodroom.com>
ENV PS1="\[\e[0;33m\]|> onion <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN apk add g++ make
RUN pip install --no-cache-dir -r requirements.txt \
    && python setup.py install
WORKDIR /
ENTRYPOINT ["onion"]

# TO run the image:
# sudo docker run -it -v /etc/onion/onion.yml:/etc/onion/onion.yml -p 9000:9000 onion:0.0.1

# TODO make sure redis and mongodb is up before running the service:
#until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
#    echo "$(date) - waiting for redis..."
#    sleep 1
#done
