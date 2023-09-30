FROM ubuntu
WORKDIR /wrkdir
COPY ~/Desktop/Networks/A1/Livestream-PubSub-Protocol/Project /wrkdir/

# for required tools
RUN apt-get update
RUN apt-get install -y net-tools netcat tcpdump inetutils-ping python3

CMD ["/bin/bash"]
