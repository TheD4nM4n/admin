FROM python:3.10.0b3-alpine3.14
MAINTAINER TheD4nM4n thed4nm4n@gmail.com

ADD admin ./

RUN apk update
RUN apk add g++ make

RUN pip install -r ./requirements.txt

CMD ["python", "-u", "core.py"]