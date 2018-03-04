import mapnik

#map layers to configure map
LAYERS = [
  {'shapefile' : 'TM_WORLD_BORDERS-0.3.shp',
   'lineColor' : 'black',
   'lineWidth' : 0.4,
   'fillColor' : '#709070',
   'labelField' : 'NAME',
   'labelSize' : 12,
   'labelColor' : 'black'
  }
]

BACKGROUND_COLOR = '#a0c0ff'

#variables for visible extent of map
BOUNDS_MIN_LAT = 35.26
BOUNDS_MAX_LAT = 71.39
BOUNDS_MIN_LONG = -10.90
BOUNDS_MAX_LONG = 41.13

#max size of image - might be smaller than bounding rectangle
MAX_WIDTH = 1600
MAX_HEIGHT = 800

#calculates max width/height of map so width is equal to max width of image(1600) and image height matches map height
extent = mapnik.Envelope(BOUNDS_MIN_LONG, BOUNDS_MIN_LAT, BOUNDS_MAX_LONG, BOUNDS_MAX_LAT)
aspectRatio = extent.width() / extent.height()

mapWidth = MAX_WIDTH
mapHeight = int(mapWidth / aspectRatio)

#if map height is larger than image height, scale down both map width and height
if mapHeight > MAX_HEIGHT:
    scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
    mapWidth = int(mapWidth * scaleFactor)
    mapHeight = int(mapHeight * scaleFactor)

#initialize map object
map = mapnik.Map(mapWidth, mapHeight)
map.background = mapnik.Color(BACKGROUND_COLOR)

#define map styles - 1 style and 1 rule for each layer
for i, src in enumerate(LAYERS):
    style = mapnik.Style()
    rule = mapnik.Rule()

    if src['fillColor'] != None:
        symbol = mapnik.PolygonSymbolizer()
        symbol.fill = mapnik.Color(src['fillColor'])
        rule.symbols.append(symbol)
    if src['lineColor'] != None:
        symbol = mapnik.LineSymbolizer()
        symbol.stroke = mapnik.Color(src['lineColor'])
        symbol.stroke_width = src['lineWidth']
        rule.symbols.append(symbol)
    if src['labelField'] != None:
        symbol = mapnik.TextSymbolizer(mapnik.Expression("[" + src['labelField'] + "]"), "DejaVu Sans Bold", src['labelSize'], mapnik.Color(src['labelColor']))

        symbol.allow_overlap = True
        rule.symbols.append(symbol)

    #appends individual rules and style combos to style
    style.rules.append(rule)

    #appends the style to map
    #args = (stylename, style)
    map.append_style("style-" + str(i+1), style)

#defines various layers???
for i, src in enumerate(LAYERS):
    layer = mapnik.Layer("layer-" + str(i+1))
    layer.datasource = mapnik.Shapefile(file=src['shapefile'])
    layer.styles.append("style-" + str(i+1))
    map.layers.append(layer)

#renders the map image
map.zoom_to_box(extent)
mapnik.render_to_file(map, "map.png", "png")
