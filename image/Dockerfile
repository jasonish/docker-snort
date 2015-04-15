FROM centos:7
MAINTAINER Jason Ish <ish@unx.ca>

RUN yum -y install \
    perl-libwww-perl \
    perl-Crypt-SSLeay \
    perl-Archive-Tar \
    perl-Sys-Syslog \
    perl-Switch \
    perl-LWP-Protocol-https \
    tar

RUN yum -y localinstall \
    https://www.snort.org/downloads/snort/daq-2.0.4.RH7.x86_64.rpm && \
    yum -y localinstall \
    https://www.snort.org/downloads/snort/snort-2.9.7.2-1.centos7.x86_64.rpm

RUN mkdir -p /opt/pulledpork && \
    cd /opt/pulledpork && \
    curl -o - -L https://github.com/shirkdog/pulledpork/archive/master.tar.gz |\
      tar zxf - --strip-components=1 && \
    chmod 755 pulledpork.pl

COPY /etc/pulledpork.conf /etc/
COPY /etc/snort/ /etc/snort/
COPY /tools/ /tools/

# Cleanup.
RUN yum clean all && \
    rm -rf /var/log/* \
    rm -rf /var/tmp/* \
    rm -rf /tmp/*

ENTRYPOINT ["/tools/boot"]

RUN /usr/sbin/snort -V
