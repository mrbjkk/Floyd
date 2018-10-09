import re
from math import radians, cos, sin, asin, sqrt
import string
import numpy as np
from numpy import *
import simplekml

INFINITY = 65535
receive = input("Please input the address of KML file with selected poins:")
toolong = int(input("Please input the defination of infinity:"))
#read the coordinates from KML file
f = open('E:\mini project\KML\Tunnel_to_End.kml', 'r')
f = open(receive, 'r')

point = []

it = re.finditer(r"<coordinates>(.*),(.*),(.*)</coordinates>", f.read())
for match in it:
    point.append(match.group(1))
    point.append(match.group(2))
for i in range(0, len(point), 1):
    point[i] = float(point[i])
#initialize two list stored longitude and latitude of each control points respectively
Long = []
Lati = []
for i in range(0, len(point), 2):
    Long.append(point[i])
for j in range(1, len(point), 2):
    Lati.append(point[j])
f.close()

#function of calculating the distance between two points on the earth
def haversine(lon1, lat1, lon2, lat2):
     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
     dlon = lon2 - lon1
     dlat = lat2 - lat1
     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
     c = 2 * asin(sqrt(a))
     r = 6371    #the mean diameter of the earth
     return c * r *1000
Dist = []  #initialize the matrix of distances

for i in range(0,len(Long), 1):
    for j in range(0, len(Lati), 1):
            Dist.append(haversine(Long[i], Lati[i], Long[j], Lati[j]))

for i in range(len(Dist)):
    if Dist[i] > toolong:
        Dist[i] = INFINITY
Dist = np.mat(Dist)
Dist = np.array(Dist).reshape(len(Long),len(Long))

#Floyd algorithm
def Floyd(p):
    Path = np.zeros((len(p),len(p)),int)
    for i in range(len(p)):
        Path[i] = i
    for k in range(len(p)):
        for i in range(len(p)):
            for j in range(len(p)):
                if(p[i][j] > p[i][k] + p[k][j]):
                    p[i][j] = p[i][k] + p[k][j]
                    Path[i][j] = k
    return Path

#function of exporting the path from start-point to end-point
def export(path):
    point = []
    point.append(len(path)-1)
    i = point[0]
    while i!=0:
        point.append(path[0][i])
        i = path[0][i]
    point.reverse()
    return point


Points = export(Floyd(Dist))

def coordlon(point):
    lon = []
    for i in range(0, len(point), 1):
        lon.append(Long[point[i]])
    return lon

def coordlat(point):
    lat = []
    for i in range(len(point)):
        lat.append(Lati[point[i]])
    return lat

Path_Lon = coordlon(Points)
Path_Lat = coordlat(Points)
#print(Dist[0][len(Dist)-1])  #print the distance between start-point and end-point

kml = simplekml.Kml()
for i in range(len(Path_Lon)-1):
    lin = kml.newlinestring(name="0", description="from P%d to P%d", 
            coords = [(Path_Lon[i], Path_Lat[i]), (Path_Lon[i+1], Path_Lat[i+1])])
    lin.style.linestyle.color = 'ff0000ff'  #set the color of path as red
    lin.style.linestyle.width = 10   #set the width of path as 10

kml.save("path3.kml")
