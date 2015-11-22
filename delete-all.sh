#!/bin/bash
gphoto2 --auto-detect | tail -n+3 | while read camera; do
    port=`echo "$camera" | tail -c+32`
        for file in $( gphoto2 --port=$port --list-files --quiet 2>/dev/null ); do
        gphoto2 --port=$port --delete-file=$file 2>/dev/null
        echo "Deleted $file"
    done
done
