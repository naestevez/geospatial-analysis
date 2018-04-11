#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:50:33 2018

@author: Alex
"""

import osgeo.ogr
count = osgeo.ogr.GetDriverCount()
list = []

for i in range(count):
    driver = osgeo.ogr.GetDriver(i)
    driverName = driver.GetName()
    if not driverName in list:
        list.append(driverName)

list.sort()

for i in list:
    print(i)
