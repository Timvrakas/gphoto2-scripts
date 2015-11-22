#!/bin/bash

capture() {
    touch "$camindex".lock
    gphoto2 --port=$port --capture-image-and-download --filename=IMG"$index"/IMG"$index"_"$camindex".CRW
    exiftool -s IMG"$index"/IMG"$index"_"$camindex".CRW >> IMG"$index"/DATA"$index"_"$camindex".txt
    echo "Transfer Done!"
    rm "$camindex".lock
}

index=`cat index`
camindex=0
rm *.lock 2>/dev/null
mkdir "IMG$index"
gphoto2 --auto-detect | tail -n+3 | while read camera; do
    port=`echo "$camera" | tail -c+32`
    capture &
    camindex=$((camindex + 1))
done

sleep 3
echo "Waiting for capture"
for pidfile in `ls *.lock`; do 
    while [ -e $pidfile ]; do sleep 0.1; done
done

echo "Reading EXIF Data"
for exiffile in `ls IMG"$index"/DATA*`; do
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
    cat $exiffile | grep -w Aperture
    echo -n "   "
    cat $exiffile | grep -w DOF
    echo -n "   "
    cat $exiffile | grep -w ISO
done

for imgfile in `ls IMG"$index"/IMG*.CRW`; do
    dcraw -4 -D -T -v $imgfile
    tifffile=`echo "$imgfile" | head -c-5`
    exiftool -overwrite_original -tagsFromFile $imgfile -a -all $tifffile.tiff
    python ExtractBayer.py -e $tifffile.tiff
done

index=$((index + 1))
echo $index > index
