FROM centos:7
MAINTAINER Jason Ish <ish@unx.ca>

ENV LUAJIT_VERSION 2.0.4
ENV DAQ_VERSION 2.0.6
ENV SNORT_VERSION 2.9.7.5
ENV PKG_CONFIG_PATH /usr/lib/pkgconfig

RUN yum -y install epel-release

# First install runtime dependencies.
RUN yum -y install \
    perl-libwww-perl \
    perl-Crypt-SSLeay \
    perl-Archive-Tar \
    perl-Sys-Syslog \
    perl-Switch \
    perl-LWP-Protocol-https \
    tar \
    libpcap \
    libpcre \
    zlib \
    libdnet \
    openssl \
    libnetfilter_queue

# Install build dependencies separately for easy rollback.
RUN rpm -qa | sort > /tmp/prebuild-rpms
RUN yum -y install \
    	   epel-release \
    	   gcc \
    	   kernel-devel \
	   flex \
	   bison \
	   make \
	   libnetfilter_queue-devel \
	   zlib-devel \
	   pcre-devel \
	   libpcap-devel \
	   openssl-devel \
	   libdnet-devel
RUN rpm -qa | sort > /tmp/postbuild-rpms

RUN cd /tmp && \
curl -O -L http://luajit.org/download/LuaJIT-${LUAJIT_VERSION}.tar.gz
RUN cd /tmp && \
curl -O -L https://www.snort.org/downloads/snort/daq-${DAQ_VERSION}.tar.gz
RUN cd /tmp && \
curl -O -L https://www.snort.org/downloads/snort/snort-${SNORT_VERSION}.tar.gz
    
RUN cd /tmp && \
    tar zxvf LuaJIT-${LUAJIT_VERSION}.tar.gz && \
    cd LuaJIT-${LUAJIT_VERSION} && \
    make PREFIX=/usr && make install PREFIX=/usr && \
    ldconfig

RUN cd /tmp && \
    tar zxvf daq-${DAQ_VERSION}.tar.gz && \
    cd daq-${DAQ_VERSION} && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    ldconfig

RUN cd /tmp && \
    tar zxvf snort-${SNORT_VERSION}.tar.gz && \
    cd snort-${SNORT_VERSION} && \
    ./configure --prefix=/usr \
    		--enable-sourcefire \
		--enable-open-appid \
		--enable-control-socket \
    && \
    make -j4 && \
    make install && \
    ln -s /usr/lib/snort_dynamicengine /usr/local/lib && \
    ln -s /usr/lib/snort_dynamicpreprocessor /usr/local/lib && \
    mkdir -p /etc/snort && \
    cp etc/*.conf /etc/snort/ && \
    cp etc/*.config /etc/snort/ && \
    cp etc/unicode.map /etc/snort/ && \
    cp etc/gen-msg.map /etc/snort/ && \
    sed \
    -e 's#^var RULE_PATH.*#var RULE_PATH /data/etc/snort/rules#' \
    -e 's#^var WHITE_LIST_PATH.*#var WHITE_LIST_PATH /data/etc/snort/rules#' \
    -e 's#^var BLACK_LIST_PATH.*#var BLACK_LIST_PATH /data/etc/snort/rules#' \
    -e 's/^\(include $.*\)/# \1/' \
    -e 's/^\(dynamicdetection.*\)/# \1/' \
    -e '$a\\ninclude $RULE_PATH/snort.rules' \
    -e 's!^# \(config logdir:\)!\1 /data/var/log/snort!' \
        etc/snort.conf > /etc/snort/snort.conf

RUN mkdir -p /opt/pulledpork && \
    cd /opt/pulledpork && \
    curl -o - -L https://github.com/shirkdog/pulledpork/archive/0.7.2.tar.gz |\
      tar zxf - --strip-components=1 && \
    chmod 755 pulledpork.pl

COPY /etc/pulledpork.conf /etc/
COPY /etc/snort/ /etc/snort/
COPY /tools/ /tools/

# Remove build dependencies.
RUN cd /tmp && \
    yum -y remove $(diff prebuild-rpms postbuild-rpms | awk '/^>/ { print $2 }')

# Cleanup.
RUN yum clean all && \
    rm -rf /var/log/* || true \
    rm -rf /var/tmp/* \
    rm -rf /tmp/*

ENTRYPOINT ["/tools/boot"]

RUN /usr/bin/snort -V
