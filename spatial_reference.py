# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 09:45:10 2018

@author: Alex
"""

#describing spatial reference systems
from osgeo import osr

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84") #spatialReference.ImportFromEPSG("4326")

print spatialReference.ExportToWkt()

#defines two spatial reference systems and transforms coordinates from src to dst
src_spatialReference = osr.SpatialReference()
src_spatialReference.SetWellKnownGeogCS("WGS84")

dst_spatialReference = osr.SpatialReference()
dst_spatialReference.SetUTM(10)

transform = osr.CoordinateTransformation(src_spatialReference, dst_spatialReference)

#converts geometry from one spatial reference to another using Transform()
geometry.Transform(transform)
