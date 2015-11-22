#! /usr/bin/env python

#
# TIFFFILE module, http://www.lfd.uci.edu/~gohlke/
# recall that Python is row major (fortran is column major)
# (https://en.wikipedia.org/wiki/Row-major_order)
# Using 0-based index scheme and matrix notation

import sys, getopt, subprocess
import tifffile as tiff
import numpy as np
# two matplotlib packages were for debugging only
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

def main():
###############################################
# parse command line arguments and set filenames
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],":?eho:s:",["help","output=",
            "exif-transfer","exif-source="])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    FileExt = ".tiff"
    DefaultOutput = True
    DoExifTransfer = False
    OverrideExifSource = False
    for option, argument in opts:
        if option in ("h", "-?", "--help"):
            print ""
            print "ExtractBayer: Extracts the 4 channel images from a combined Bayer Pattern Image"
            print "usage: ./ExtractBayer.py [options] INPUT_IMAGE.tiff"
            print ""
            print "Options:"
            print "-o   --output=           Specify output prefix"
            print "-s   --exif-source=      Select file to pull EXIF data from"
            print "-e   --exif-transfer     transfer EXIF data to created images"
            sys.exit(2)
        elif option in ("-o", "--output"):
            DefaultOutput = False
            OutputRoot = argument
        elif option in ("-s", "--exif-source"):
            OverrideExifSource = True
            ExifSourceFile = argument
        elif option in ("-e", "--exif-transfer"):
            DoExifTransfer = True
        else:
            assert False, "unhandled option"

            
    if len(args)<1:
        print ""
        print "ExtractBayer: Extracts the 4 channel images from a combined Bayer Pattern Image"
        print "usage ./ExtractBayer.py [options] INPUT_IMAGE.tiff"
        print ""
        print "Options:"
        print "-o   --output=           Specify output prefix"
        print "-s   --exif-source=      Select file to pull EXIF data from"
        print "-e   --exif-transfer     transfer EXIF data to created images"
        sys.exit(2)

# check for ".tif[f]" suffix, if not found, need to add
    InputFile = args[0]
    idx = InputFile.find(".tif")
    if (idx > 1):
        InputRoot = InputFile[:idx]
        InputExt = InputFile[idx:]
        InputFile = InputRoot+InputExt
    else:
        InputRoot = InputFile
        Inputfile = InputRoot + InputExt

    # handle default OutputFile
    if ( DefaultOutput ):
        OutputRoot = InputRoot

    print "Input file is %s." % InputFile
    print "Output file rootname is %s." % OutputRoot
        
    # handle Exif transfer source
    if ( DoExifTransfer ):
        if ( OverrideExifSource is False ):
            ExifSourceFile = InputFile
        print >> sys.stderr,"Will transfer Exif tags from ",ExifSourceFile,"."
    
    if len(args)>1:
        print "Extra text being ignored: ",args[1:]




###############################################
     
# TIFFFILE reads image out in (nr,nc) format, not (nx,ny)
    img = np.array(tiff.imread(InputFile))
    (ny,nx) = img.shape   # ny = number of rows, nx = number of columns
    (nr,nc) = img.shape 

# create arrays which are 0 if an odd pixel and 1 if odd)
    cpix = np.arange(0,nc) % 2
    rpix = np.arange(0,nr) % 2
    ceven = (cpix==0).nonzero()
    codd = (cpix==1).nonzero()
    reven = (rpix==0).nonzero()
    rodd = (rpix==1).nonzero()

# the slicing introduces an extra dimension (with only one element) - remove
    rg = np.squeeze(img[reven,:])
    gb = np.squeeze(img[rodd,:])

# http://www.peter-cockerell.net/Bayer/bayer.html
# assume that 0 0 is in upper left corner of picture.
# each group of four pixel is as follows, repeating rightward and downward:
#   red (0 0)     green (0 1)
#   green2 (1 0)  blue  (1 1)
#
    print "Writing out Bayer channels using rootname %s." % OutputRoot
    red = np.squeeze(rg[:,ceven])
    OutputFile = OutputRoot+"_red"+InputExt
    tiff.imsave(OutputFile,red)
    if ( DoExifTransfer ):
        ExifTransfer( ExifSourceFile, OutputFile )
        
    green1 = np.squeeze(rg[:,codd])
    OutputFile = OutputRoot+"_gr1"+InputExt
    tiff.imsave(OutputFile,green1)
    if ( DoExifTransfer ):
        ExifTransfer( ExifSourceFile, OutputFile )
        
    green2 = np.squeeze(gb[:,ceven])
    OutputFile = OutputRoot+"_gr2"+InputExt
    tiff.imsave(OutputFile,green2)
    if ( DoExifTransfer ):
        ExifTransfer( ExifSourceFile, OutputFile )

    blue = np.squeeze(gb[:,codd])
    OutputFile = OutputRoot+"_blue"+InputExt
    tiff.imsave(OutputFile,blue)
    if ( DoExifTransfer ):
        ExifTransfer( ExifSourceFile, OutputFile )

    exit(0)




def ExifTransfer( SourceFile, TargetFile ):
    mycmd = "exiftool"
    myarg = " -overwrite_original -tagsFromFile "+SourceFile+" -a -all "+TargetFile 
    try:
        print >>sys.stderr, "transferring EXIF values: ",mycmd+myarg
        ReturnCode = subprocess.call(mycmd + myarg, shell=True)
        if ReturnCode < 0:
            print >>sys.stderr, "Child was terminated by signal", -ReturnCode
        else:
            print >>sys.stderr, "Child returned", ReturnCode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e



if __name__ == "__main__":
    main()
