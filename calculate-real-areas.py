#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:32:46 2018

@author: Alex
"""
from osgeo import ogr
from osgeo import osr
import shapely.wkt

wkt = "POLYGON((-73.973057 40.764356, -73.981898 40.768094, -73.958209 40.800621, -73.949282 40.796853, -73.973057 40.764356))"
outline = shapely.wkt.loads(wkt)

#result in square degrees (meaningless number)
print outline.area

#to calculate real area, must convert unprojected long/lat to "equal area" map projection in meters
#create ogr geometry object
polygon = ogr.CreateGeometryFromWkt(wkt)

src_spatialReference = osr.SpatialReference()
src_spatialReference.ImportFromEPSG(4326)

dst_spatialReference = osr.SpatialReference()
dst_spatialReference.ImportFromEPSG(54009)

transform = osr.CoordinateTransformation(src_spatialReference, dst_spatialReference)

#transform geometry from WGS84 to Mollweide Porjection and convert back to Shapely geometry
polygon.Transform(transform)

outline = shapely.wkt.loads(polygon.ExportToWkt())
print outline.area


 
