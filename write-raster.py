#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 22:31:09 2018

@author: Alex
"""

from osgeo import gdal
from osgeo import osr
import random
import numpy

driver = gdal.GetDriverByName("EHdr")

#parameters (name of file, num of rows, number of columns, number of raster bands, type of data)
dstfile = driver.Create("Example Raster", 180, 360, 1, gdal.GDT_Int16)

#specify spatial reference
spatialReference = osr.SpatialReference() 
spatialReference.SetWellKnownGeogCS("WGS84")

dstfile.SetProjection(spatialReference.ExportToWkt())

#georeference the raster data to the Earth's surface
originX = -180
originY = 90
cellWidth = 0.25
cellHeight = 0.25

geoTransform = [originX, cellWidth, 0, originY, 0, -cellHeight]
dstfile.SetGeoTransform(geoTransform)

#create raster data by creating an array of values between 1 - 100
data = []
for row in range(360):
    row_data = []
    for col in range(180):
        row_data.append(random.randint(1, 100))
    data.append(row_data)
        
#convert data array into numpy array with 16 bit signed integer
array = numpy.array(data, dtype=numpy.int16)


#saves into the file
band=[]
band.WriteArray(array)

band.SetNoDataValue(-500)
del dstfile



