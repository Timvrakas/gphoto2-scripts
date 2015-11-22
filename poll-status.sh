#!/bin/bash

getexif() {
    touch "$camindex".lock
    gphoto2 --port=$port --capture-preview --filename=preview"$camindex".jpg
    exiftool -s preview"$camindex".jpg 1> EXIF"$camindex".txt 2>/dev/null
    rm "$camindex".lock preview"$camindex".jpg
}

rm *.lock EXIF* preview* 2>/dev/null
camindex=0
gphoto2 --auto-detect | tail -n+3 | while read camera; do
    port=`echo "$camera" | tail -c+32`
    getexif &
    camindex=$((camindex + 1))
done

sleep 1
echo "Saving EXIF Header to File"
for pidfile in `ls *.lock`; do 
    while [ -e $pidfile ]; do sleep 0.1; done
done

echo "Reading EXIF Data"
for exiffile in `ls EXIF*`; do
    echo -n "Camera:" 
    echo $exiffile | tail -c6 | head -c1
    echo
    echo -n "   "
    cat $exiffile | grep -w FocalLength
    echo -n "   "
    cat $exiffile | grep -w DateTimeOriginal
    echo -n "   "
    cat $exiffile | grep -w ExposureTime
    echo -n "   "
    cat $exiffile | grep -w ApertureValue
    echo -n "   "
    cat $exiffile | grep -w DOF
    echo -n "   "
    cat $exiffile | grep -w ISO
    rm $exiffile
done


