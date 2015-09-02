FROM cravattlab/cravattdb_base

MAINTAINER Radu Suciu <radusuciu@gmail.com>

ADD / /home/cravatt
VOLUME /home/cravatt/uploads

RUN adduser --disabled-password --gecos '' cravattdb
RUN chown -R cravattdb /home/cravatt
USER cravattdb

WORKDIR /home/cravatt
RUN npm install
RUN bower install -F --config.analytics=false
RUN virtualenv env && . env/bin/activate && pip install -r requirements.txt