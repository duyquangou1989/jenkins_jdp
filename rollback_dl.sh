#!/bin/bash
dladdonspath=$1
findbk=`ls -t /data/backup | grep 'addons_bk' | head -n1`
if [ -d /data/backup/${findbk}/dl-addons13 ];
then
    if [ -d ${dladdonspath} ]; then
        echo "Rsync: /data/backup/${findbk}/dl-addons13 --> ${dladdonspath} "
        cd /data/backup/${findbk}/dl-addons13; rsync -avz -r * ${dladdonspath}/
    else
        exit 1
    fi
fi