#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 22:41:44 2018

@author: Alex
"""

import osgeo.ogr

shapefile = osgeo.ogr.Open("tl_2017_us_zcta510.shp")
layer = shapefile.GetLayer(0)