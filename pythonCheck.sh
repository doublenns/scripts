#!/usr/bin/env bash -
for i in $(cat serverList) ; do

        ssh     -o ConnectTimeout=10 \
                -o UserKnownHostsFile=/dev/null \
                -o StrictHostKeyChecking=no \
                -o PreferredAuthentications=publickey \
                $(whoami)@"$i" \
		'echo -n "$(hostname) "; python --version';

done
