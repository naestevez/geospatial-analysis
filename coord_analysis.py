import pyproj

geod = pyproj.Geod(ellps="WGS84")

#prompt user to enter desired coordinates
def get_coord(prompt):
    while True:
        s = raw_input(prompt + " (lat,long): ")
        if "," not in s: continue
        s1, s2 = s.split(",", 1)
        try:
            latitude = float(s1.strip())
        except ValueError:
            continue
        try: longitude = float(s2.strip())
        except ValueError:
            continue
        return latitude, longitude

# lat1,long1 = get_coord("Starting coordinate")
# lat2,long2 = get_coord("Ending coordinate")
#
# #calculate distance between these two coordinates
# heading1,heading2,distance = geod.inv(long1, lat1, long2, lat2)
#
# print "Heading = %0.2f degrees" % heading1
# print "Inverse heading = %0.2f degrees" % heading2
# print "Distance = %0.2f kilometers" % (distance/1000)

def get_num(prompt):
    while True:
        s = raw_input(prompt + ": ")
        try:
            value = float(s)
        except ValueError:
            continue
        return value

#prompts user for starting coordinate, distance and heading
sLat, sLong = get_coord("Starting coordinate")
distance = get_num("Distance in kilometers") * 1000
heading = get_num("Heading")

#calculate ending coordinate and inverse heading and print it out
eLong, eLat, iHeading = geod.fwd(sLong, sLat, heading, distance)

print "End point = (%0.4f,%0.4f)" % (eLat, eLong)
print "Inverse heading = %0.2f degrees" % iHeading
