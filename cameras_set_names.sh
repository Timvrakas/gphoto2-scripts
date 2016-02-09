#! /bin/bash

# This script allows the user to name the cameras LEFT and RIGHT for use
# in image naming, etc. downstream.  The script loops over the available 
# cameras, taking a picture, informing the user of the camera name, and
# allowing the camera to be renamed.
#
# The name of the camera is the "ownername" field in the Canon config tree.
# Perversely, this is translated into OnwerName in the EXIF header.


TestImageName='test.jpg'
/bin/rm -f ${TestImageName}

#
echo "changing camera formats to JPG"
cameras_change_jpg.py

#
for port in `cameras_list_ports.py`; do

   echo "Taking a test image with the camera on port ${port}."
   echo "Look for the preview image on the back of the camera."
   sleep 1
   ok=0
   while [ $ok != 1 ]; do
      gphoto2 --port=${port} --get-config=ownername
      gphoto2 --port=${port} --capture-image-and-download --filename=${TestImageName} --force-overwrite
      OwnerName=`exiftool -s $TestImageName | grep OwnerName | cut -f2,2 -d':' | sed -s 's/ //g'`
      echo "This camera is named $OwnerName.  Ok to proceed (y,N)?"
      read ans
      if [ $ans == "y" ]; then
         ok=1
      else
         echo "Enter the new name for the camera."
         read NewName
         gphoto2 --port=${port} --set-config ownername=${NewName}
      fi
   done
done


# clean-up
echo "changing camera formats to RAW"
cameras_change_raw.py
/bin/rm -f ${TestImageName}
