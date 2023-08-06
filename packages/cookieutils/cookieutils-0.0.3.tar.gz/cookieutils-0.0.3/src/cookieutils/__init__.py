# -*- coding: utf-8 -*-
__version__ = "0.0.3"
import os
if os.name=='nt': # windows
  __operating_system__ = "windows"
else: #unix
  __operating_system__ = "unix"


def get_version():
    return __version__

def get_os():
    return __operating_system__