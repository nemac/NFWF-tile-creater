#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
#  $Id$
#
# Project:  Google Summer of Code 2007, 2008 (http://code.google.com/soc/)
# Support:  BRGM (http://www.brgm.fr)
# Purpose:  Convert a raster into TMS (Tile Map Service) tiles in a directory.
#           - generate Google Earth metadata (KML SuperOverlay)
#           - generate simple HTML viewer based on Google Maps and OpenLayers
#           - support of global tiles (Spherical Mercator) for compatibility
#               with interactive web maps a la Google Maps
# Author:   Klokan Petr Pridal, klokan at klokan dot cz
# Web:      http://www.klokan.cz/projects/gdal2tiles/
# GUI:      http://www.maptiler.org/
#
###############################################################################
# Copyright (c) 2008, Klokan Petr Pridal
# Copyright (c) 2010-2013, Even Rouault <even dot rouault at mines-paris dot org>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# ******************************************************************************

from __future__ import print_function, division

import math
from multiprocessing import Pipe, Pool, Process, Manager
import os
import tempfile
import threading
import shutil
import sys
from uuid import uuid4
from xml.etree import ElementTree

from osgeo import gdal
from osgeo import osr

try:
    #from PIL import Image
    import numpy
    import osgeo.gdal_array as gdalarray
    numpy_available = True
except ImportError:
    # 'antialias' resampling is not available
    numpy_available = False


# file = '/Users/daveism/Downloads/75.png'
# ds = gdal.Open(file, gdal.GA_Update)
# band1 = ds.GetRasterBand(1)
# band2 = ds.GetRasterBand(2)
# band3 = ds.GetRasterBand(3)
#
# band1.SetNoDataValue(0)
# band2.SetNoDataValue(0)
# band3.SetNoDataValue(0)
#


# walk_dir = '/Users/daveism/nfwf_test_tiles/south_florida'
walk_dir = sys.argv[1]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
# print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    for filename in files:
        file_path = os.path.join(root, filename)
        ext = os.path.splitext(file_path)[-1].lower()

        if ext == ".png":
            ds = gdal.Open(file_path, gdal.GA_ReadOnly)
            mem_drv = gdal.GetDriverByName('MEM')
            alphaband = ds.GetRasterBand(1).GetMaskBand()

            alpha = alphaband.ReadRaster()
            data = ds.ReadAsArray()
            # print(numpy.sum(data) )
            fullcount = numpy.count_nonzero(data)
            count255 = numpy.count_nonzero(data==255)

            # print(len(alpha))
            # print(alpha.count('\x00'.encode('ascii')))

            # Detect totally transparent tile and skip its creation
            if fullcount == count255:
                os.remove(file_path)
                print('Deleting all 255 file %s (full path: %s)' % (filename, file_path))
            # else:
            #     print('\t- mixed values file %s (full path: %s)' % (filename, file_path))
