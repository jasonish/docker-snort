FROM fedora:23
MAINTAINER Jason Ish <ish@unx.ca>

ENV DAQ_VERSION 2.0.6
ENV SNORT_VERSION 2.9.7.6

RUN dnf -y install \
https://www.snort.org/downloads/snort/daq-${DAQ_VERSION}-1.f21.x86_64.rpm \
https://www.snort.org/downloads/snort/snort-openappid-${SNORT_VERSION}-1.f21.x86_64.rpm

RUN ln -s /usr/lib64/snort-${SNORT_VERSION}_dynamicengine \
       /usr/local/lib/snort_dynamicengine && \
    ln -s /usr/lib64/snort-${SNORT_VERSION}_dynamicpreprocessor \
       /usr/local/lib/snort_dynamicpreprocessor

# Install pulledpork.
RUN dnf -y install tar \
	perl-libwww-perl \
	perl-Crypt-SSLeay \
	perl-Archive-Tar \
	perl-Sys-Syslog \
	perl-Switch \
	perl-LWP-Protocol-https && \
    mkdir -p /opt/pulledpork && \
    cd /opt/pulledpork && \
    curl -o - -L https://github.com/shirkdog/pulledpork/archive/0.7.2.tar.gz |\
      tar zxf - --strip-components=1 && \
    chmod 755 pulledpork.pl

RUN sed -i \
    -e 's#^var RULE_PATH.*#var RULE_PATH /data/etc/snort/rules#' \
    -e 's#^var WHITE_LIST_PATH.*#var WHITE_LIST_PATH /data/etc/snort/rules#' \
    -e 's#^var BLACK_LIST_PATH.*#var BLACK_LIST_PATH /data/etc/snort/rules#' \
    -e 's/^\(include $.*\)/# \1/' \
    -e 's/^\(dynamicdetection.*\)/# \1/' \
    -e '$a\\ninclude $RULE_PATH/snort.rules' \
    -e 's!^# \(config logdir:\)!\1 /data/var/log/snort!' \
        /etc/snort/snort.conf

COPY /etc /etc
COPY /tools/ /tools/

# Cleanup.
RUN dnf clean all && \
    rm -rf /var/log/* || true \
    rm -rf /var/tmp/* \
    rm -rf /tmp/*

ENTRYPOINT ["/tools/boot"]

RUN /usr/sbin/snort -V
