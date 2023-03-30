FROM ubuntu

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

RUN echo "#######"
# Update Ubuntu Software repository
RUN apt update
RUN apt upgrade -y
RUN apt install net-tools iproute2 git pkg-config make gcc bison flex sudo kmod -y

#RUN apt install --reinstall linux-image-$(uname -r) -y;
#RUN apt install --reinstall linux-modules-$(uname -r) -y;
#RUN apt install --reinstall linux-modules-extra-$(uname -r) -y;


COPY all iproute2

RUN cd  all/iproute2 && ./configure #&& make && make install && sudo modprobe macsec
RUN make -C all/iproute2
RUN make install -C all/iproute2
#RUN modprob macsec
RUN insmod all/macsec.ko

CMD ["bash"]
