#!/usr/bin/env python

# This script lists the USB ports where cameras are found. Resulting
# ports are printed on a single line (space-delimited)
#

# based on and using code snippets from:
#
# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
#

from __future__ import print_function

import logging
import sys

import gphoto2 as gp


def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    
    context = gp.gp_context_new()
    camera_list = gp.check_result(gp.gp_camera_autodetect(context))

    port_list = []
    # loop through camera list
    for index, (name, addr) in enumerate(camera_list):
        port_list.append(addr)

    for port in port_list:
        print(port,end=' ')

    return 0

if __name__ == "__main__":
    sys.exit(main())
