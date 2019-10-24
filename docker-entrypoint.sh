#! /bin/bash

if [[ "${PGID}" ]]; then
    groupmod -o -g "${PGID}" snort > /dev/null 2>&1
fi

if [[ "${PUID}" ]]; then
    usermod -o -u "${PUID}" snort > /dev/null 2>&1
fi

if ! test -e /etc/snort/snort.conf; then
    echo "Populating /etc/snort/..."
    cp -a /etc/snort.skel/* /etc/snort/
fi

chown -R snort /var/log/snort

exec $@
