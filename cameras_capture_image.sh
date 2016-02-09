#!/bin/bash


capture() {
   touch ${RootName}.lock
   FileName=${RootName}${seconds}
   gphoto2 --port=${port} --capture-image-and-download --filename=${FileName}.CRW
   echo $FileName
   /bin/rm ${RootName}.lock
}

seconds=`date +%s`
for port in `cameras_list_ports.py`; do
    gphoto2 --port=${port} --get-config=ownername
    RootName=`gphoto2 --port=${port} --get-config=ownername | grep Current | cut -f2,2 -d':' | sed -e 's/ //g' `
    LastName=$RootName
    capture &
done

sleep 1
echo "Waiting for file transfers to finish..."
for pidfile in `ls *.lock`; do 
    while [ -e $pidfile ]; do sleep 0.1; done
done

exit
