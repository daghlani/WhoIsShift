# STEP 1
#FROM python:3.8 AS Base
FROM python:3.8 AS Base
LABEL creator="Ali Daghlani <alidaghlani@gmail.com>"
ENV PYTHONUNBUFFERED 1
RUN mkdir /WISH
WORKDIR /WISH
ADD requirements.txt /WISH
RUN pip3 install -r requirements.txt

# STEP 2
FROM Base AS wish
ENV TZ="Asia/Tehran"
RUN date
ENV PYTHONUNBUFFERED 1
WORKDIR /WISH
ADD . /WISH
#RUN python manage.py collectstatic
#VOLUME /FDASH/st
EXPOSE 9001
ENTRYPOINT /bin/bash run.sh
