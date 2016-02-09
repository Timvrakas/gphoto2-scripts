#! /bin/bash

# This script loops over the camera list and reports the Focal Length.
# The user can change the focal length until the desired settings are
# reached.
# 
# The gphoto2 command is filtered to /dev/out to cut back on the chatter.
#
# The script assumes that there user is either aware of the camera names 
# (ownername) for each camera, or is at least paying attention to the order
# in which the cameras are triggered.


TestImageName='test.jpg'
/bin/rm -f ${TestImageName}

#
echo "Changing camera formats to JPG..."
echo " "
cameras_change_jpg.py
echo " "
echo " "
echo " "

#
ok=0
PortList=`cameras_list_ports.py`
while [ $ok != 1 ]; do
   echo "Taking images for cameras on ports: $PortList"
   for port in $PortList; do
      gphoto2 --port=${port} --capture-image-and-download --filename=${TestImageName} --force-overwrite ${filter_mode} >&/dev/null
      FocalLength=`exiftool -s $TestImageName | egrep -i \^FocalLength\ | cut -f2,2 -d':' | sed -s 's/ //g'`
      OwnerName=`exiftool -s $TestImageName | grep OwnerName | cut -f2,2 -d':' |
 sed -s 's/ //g'`
      ans="N"
      echo "Camera $OwnerName has a focal length of $FocalLength."

   done
   echo " "
   echo " "
   echo "Satified with settings (if not, change before answering): (y,N)?"
   echo " "
   echo " "
   read ans
   if [ $ans == "y" ]; then
      ok=1
   fi
done


# clean-up
echo " "
echo " "
echo " "
echo "Changing camera formats to RAW..."
echo " "
cameras_change_raw.py
/bin/rm -f ${TestImageName}
