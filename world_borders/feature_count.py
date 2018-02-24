#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 21:55:10 2018

@author: Alex
"""

import osgeo.ogr

shapefile = r"TM_WORLD_BORDERS-0.3.shp"
dataSource = osgeo.ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
layer = dataSource.GetLayer(0)
layerDefn = layer.GetLayerDefn()
feature_count = layer.GetFeatureCount()

print "Feature count: ", feature_count
