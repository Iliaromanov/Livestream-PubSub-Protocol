FROM ubuntu
WORKDIR /wrkdir
COPY ./Project /wrkdir/
COPY ./setup-wireshark.sh /wrkdir/

# for required tools
RUN apt-get update
RUN apt-get install -y net-tools netcat tcpdump inetutils-ping python3

# for wireshark
RUN mkdir /tmp/foobar
RUN chmod 700 /tmp/foobar
RUN chmod 777 ./setup-wireshark.sh

CMD ["/bin/bash"]
