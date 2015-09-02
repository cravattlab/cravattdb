FROM cravattlab/cravattdb_base

MAINTAINER Radu Suciu <radusuciu@gmail.com>

# Clone repos in
WORKDIR /home/cravattdb

# Create user with non-root privileges
RUN adduser --disabled-password --gecos '' cravattdb
RUN chown -R cravattdb /home/cravattdb

# Setup cimage
RUN ln -s /home/cravattdb/cimage-minimal/cimage2 /usr/local/bin
RUN ln -s /home/cravattdb/cimage-minimal/cimage_combine /usr/local/bin
ENV CIMAGE_PATH /home/cravattdb/cimage-minimal

# Setup CravattDB
USER cravattdb
ENV PATH /home/cravattdb/cravatt-ip2/env/bin:$PATH

ADD /cravatt-ip2/start.sh /home/cravattdb/start.sh

CMD [ "/bin/bash", "/home/cravattdb/start.sh" ]