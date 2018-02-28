import mapnik

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

BACKGROUND COLOR = '#a0c0ff'

BOUNDS_MIN_LAT = 35.26
BOUNDS_MAX_LAT = 71.39
BOUNDS_MIN_LONG = -10.90
BOUNDS_MAX_LONG = 41.13

MAX_WIDTH = 1600
MAX_HEIGHT = 800

extent = mapnik.Envelope(BOUNDS_MIN_LONG,BOUNDS_MIN_LAT, BOUNDS_MAX_LONG, BOUNDS_MAX_LAT)
aspectRatio = extent.width() / extent.height

mapWidth = MAX_WIDTH
mapHeight = int(mapWidth / aspectRatio)

if mapHeight > MAX_HEIGHT:
    scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
    mapWidth = int(mapWidth * scaleFactor)
    mapHeight = int(mapHeight * scaleFactor)
    
