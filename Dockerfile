FROM python:3.7.6
MAINTAINER "felix"
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"
WORKDIR /root

COPY run.py run.py
RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip
RUN pip --no-cache-dir install  -i ${PIPURL} gunicorn==20.0.4
RUN pip --no-cache-dir install  -i ${PIPURL} flask==1.1.2
RUN pip --no-cache-dir install  -i ${PIPURL} gevent==20.6.2

CMD gunicorn  -c gunicorn.conf run:app
