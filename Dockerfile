FROM ubuntu:22.04

# for the local apt-cacher-ng proxy
#RUN echo 'Acquire::HTTP::Proxy "http://192.168.1.226:3142";' >> /etc/apt/apt.conf.d/01proxy && \
#    echo 'Acquire::HTTPS::Proxy "false";' >> /etc/apt/apt.conf.d/01proxy

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache docker

COPY main.py /main.py

CMD ["python3", "/main.py"]