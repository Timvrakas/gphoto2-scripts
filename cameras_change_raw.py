#!/usr/bin/env python

# based on and using code snippets from:
#
# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#

from __future__ import print_function

import logging
import sys

import gphoto2 as gp

jpgFormat = "Small Normal JPEG"
rawFormat = "RAW"

def get_config_value (config, config_name):
    OK, config_child = gp.gp_widget_get_child_by_name(config,config_name)
    if OK >= gp.GP_OK:
        value = gp.check_result(gp.gp_widget_get_value(config_child))

    return value

def set_config_value (camera, config, context, config_name, value):
    OK, config_child = gp.gp_widget_get_child_by_name(config,config_name)
    if OK >= gp.GP_OK:
        gp.check_result(gp.gp_widget_set_value(config_child, value))
        gp.check_result(gp.gp_camera_set_config(camera, config, context))

        return True
    else:
        return False


def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    
    context = gp.gp_context_new()
    camera_list = gp.check_result(gp.gp_camera_autodetect(context))
#    gp.check_result(gp.gp_camera_init(camera, context))
    
#    camera_list = GetCameraList(context)


    # loop through camera list
    for index, (name, addr) in enumerate(camera_list):
        print('Processing camera {:d}:  {:s}  {:s}'.format(index, addr, name))

    # search ports for camera port name and match to this iteration
        port_info_list = gp.check_result(gp.gp_port_info_list_new())
        gp.check_result(gp.gp_port_info_list_load(port_info_list))
        idx = gp.check_result(gp.gp_port_info_list_lookup_path(port_info_list, addr))

    # open this camera and associated context
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_set_port_info(camera,port_info_list[idx]))
        gp.check_result(gp.gp_camera_init(camera,context))

    # get camera configuration
        config = gp.check_result(gp.gp_camera_get_config(camera,context))

    # grab current value of imageformat and change to JPG
        image_format_old = get_config_value(config,'imageformat')
        set_config_value(camera,config,context,'imageformat',rawFormat)
        image_format = get_config_value(config,'imageformat')

        print('Changed image format from {:s} to {:s}'.format(image_format_old,image_format))

    # close this camera
        gp.check_result(gp.gp_camera_exit(camera,context))
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
