#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:50:33 2018

@author: Alex
"""

import ogr
count = ogr.GetDriverCount()
list = []

for i in range(count):
    driver = ogr.GetDriver(i)
    driverName = driver.GetName()
    if not driverName in list:
        list.append(driverName)
        
list.sort()

for i in list:
    print i
