#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 19:49:26 2018

@author: Alex
"""

import mapnik
from mapnik import LineSymbolizer

map = mapnik.Map(1200, 600)
map.background = mapnik.Color("#e0e0ff")

layer = mapnik.Layer("countries")
layer.datasource = mapnik.Shapefile(file="TM_WORLD_BORDERS-0.3.shp")
layer.styles.append("country_style")
map.layers.append(layer)

fill_symbol = mapnik.PolygonSymbolizer()
fill_symbol.fill = mapnik.Color("#60a060")
line_symbol = LineSymbolizer()
line_symbol.stroke = mapnik.Color("black")
line_symbol.stroke_width = 0.5


rule = mapnik.Rule()
rule.symbols.append(fill_symbol)
rule.symbols.append(line_symbol)

style = mapnik.Style()
style.rules.append(rule)

map.append_style("country_style", style)

map.zoom_all()
mapnik.render_to_file(map, "map.png", "png")
