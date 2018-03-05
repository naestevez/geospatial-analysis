import mapnik

#create map
m = mapnik.Map(600,300)
m.background = mapnik.Color('steelBlue')

#create styles
s = mapnik.Style() #style object to hold rules
r = mapnik.Rule() #rule object to hold symbolizers

#to fill a polygon
polygon_symbolizer = mapnik.PolygonSymbolizer()
polygon_symbolizer.fill = mapnik.Color('#f2eff9')
r.symbols.append(polygon_symbolizer) #add symbolizer to rule

#to outline a polygon
line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
line_symbolizer.stroke_width = 0.1
r.symbols.append(line_symbolizer) #add symbolizer to rule

#add rule to the style
s.rules.append(r)

#add style to map
m.append_style("My Style", s)

#create a datasource
datasource = mapnik.Shapefile(file='110m-admin-0-countries/ne_110m_admin_0_countries.shp')

#prints full coordinate bounds of the data
print(datasource.envelope())

#create a layer
layer = mapnik.Layer('world')
#attach datasource to layer
layer.datasource = datasource

#style must be appended to layer
layer.styles.append('My Style')

#append layer to map and zoom to extent of layer
m.layers.append(layer)
m.zoom_all()

#write the data to a png image
mapnik.render_to_file(m, 'world.png', 'png')
