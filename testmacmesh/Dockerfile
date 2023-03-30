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


COPY all all
WORKDIR all

RUN cd  iproute2 && ./configure #&& make && make install && sudo modprobe macsec
RUN make -C iproute2
RUN make install -C iproute2
#RUN insmod macsec.ko

COPY variables.conf variables.conf
COPY run_macsec.sh run_macsec.sh

ENTRYPOINT ["./run_macsec.sh"]


#CMD ["bash"]
