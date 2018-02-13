#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:31:28 2018

@author: Alex
"""

from osgeo import ogr
from osgeo import osr

driver = ogr.GetDriverByName("ESRI Shapefile")
destFile = driver.CreateDataSource("test-shapefile")

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84") #WGS84 - standard for lat and long

layer = destFile.CreateLayer("layer", spatialReference)

#create attribute and store in layer
field = ogr.FieldDefn("NAME", ogr.OFTString)
field.setWidth(100)
layer.CreateField(field)

#define simple polygon
wkt = "POLYGON((23.4 38.9, 23.5 38.9, 23.5 38.8, 23.4 38.9))"
polygon = ogr.CreateGeometryFromWkt(wkt)

feature = ogr.Feature(layer.GetLayerDefn())
feature.SetGeometry(polygon)
feature.SetField("NAME", "My Polygon")

layer.CreateFeature(feature)
feature.Destroy()

destFile.Destroy()
