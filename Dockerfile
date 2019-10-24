FROM centos:7
MAINTAINER Jason Ish <ish@unx.ca>

ENV SNORT_VERSION 2.9.15

# Do all the yum stuff within one RUN to keep the size down.
RUN yum -y install epel-release && \
        yum -y install libdnet && \
        yum -y install \
        https://www.snort.org/downloads/archive/snort/snort-openappid-${SNORT_VERSION}-1.centos7.x86_64.rpm && \
        yum clean all

RUN ln -s libdnet.so.1 /usr/lib64/libdnet.1
RUN mkdir /usr/local/lib/snort_dynamicrules

RUN touch /etc/snort/rules/white_list.rules \
        /etc/snort/rules/black_list.rules

# Comment out all rule includes.
RUN sed -i "s/include \$RULE\_PATH/#include \$RULE\_PATH/" /etc/snort/snort.conf

# But keep local.rules enabled.
RUN sed -i "s/\#include \$RULE_PATH\/local\.rules/include \$RULE_PATH\/local\.rules/" /etc/snort/snort.conf

# Create an empty local.rules.
RUN touch /etc/snort/rules/local.rules

# For some reason the default config is looking in /etc/rules.
RUN sed -i "s#var WHITE_LIST_PATH \.\.\/rules#var WHITE_LIST_PATH /etc/snort/rules#" /etc/snort/snort.conf
RUN sed -i "s#var BLACK_LIST_PATH \.\.\/rules#var BLACK_LIST_PATH /etc/snort/rules#" /etc/snort/snort.conf

RUN sed -i "s/# output unified2:/output unified2:/" /etc/snort/snort.conf
RUN echo "output alert_full: alert.full" >> /etc/snort/snort.conf
RUN echo "output alert_fast: alert.fast" >> /etc/snort/snort.conf

RUN cp -a /etc/snort /etc/snort.skel

RUN /usr/sbin/snort -V

COPY /docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
