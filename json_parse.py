import json
import sys
from collections import defaultdict
import logging
import csv
import math

logging.basicConfig(filename='logfile.log',level=logging.DEBUG)

# -*- coding: utf-8 -*-
with open("/Users/gorkeralp/Dropbox/Okul/Research/QPU/kadikoy_yol.json") as data_file:
    data = json.load(data_file)
    #print type(data)
    #print len(data)
    #print data.keys()
    #print (data)
    #print type(coord)
    print('------')
    countX=0
    countY=0



    def FindNearestPointInMap(car_data):
        processed_car_data = ProcessCarData(car_data)
        minPoints = [10000,10000,10000]
        closestPoints = [0,0,0]
        grid_points = []
        for index in range(len(processed_car_data)):
            latGrid,longGrid = findGrid(processed_car_data[index][0],processed_car_data[index][1],minLattituteCoord,minLongtitudeCoord)
            ##point Tuple in the grid

            grid_points.append(coord_gridid_dict[(latGrid,longGrid)]) ##points in coordinate
            grid_points.append(coord_gridid_dict[(latGrid+1,longGrid)]) #east
            grid_points.append(coord_gridid_dict[(latGrid-1,longGrid)])  #west
            grid_points.append(coord_gridid_dict[(latGrid+1, longGrid+1)]) #ne
            grid_points.append(coord_gridid_dict[(latGrid-1, longGrid+1)]) #nw
            grid_points.append(coord_gridid_dict[(latGrid, longGrid+1)]) #north
            grid_points.append(coord_gridid_dict[(latGrid, longGrid-1)]) #south
            grid_points.append(coord_gridid_dict[(latGrid+1, longGrid-1)]) #southeast
            grid_points.append(coord_gridid_dict[(latGrid-1, longGrid-1)]) #southeast

            if not grid_points:
                print str(processed_car_data[index][0]),str(processed_car_data[index][1])

            logging.info('grid_points:'+str(grid_points))
            for eachpoint in grid_points:
                for eachtup in eachpoint:
                    res = Haversine(processed_car_data[index],eachtup) #first car points
                    if minPoints[index] > res:
                        minPoints[index] = res
                        closestPoints[index]=((eachtup,processed_car_data[index],res))
                #haversine
        print closestPoints
        return closestPoints

    def findGrid(lattitude,longtitude,minlattitude,minlongtitude): #takes normalized inputs
        decPointLat = long(lattitude * 100000) - minlattitude
        decPointLong = long(longtitude * 100000) - minlongtitude
        decPointLat //= 65.13 #12.7207 #lattitute
        decPointLong //= 93.77 #9.157  #longtitude
        #gridnumber =  decPointLat * 1024 + decPointLong
        #ll / value #corresponds to value
        #gridnum = long(ll / 2**grids)
        return long(decPointLat),long(decPointLong)

    def FillGPSInfo(lattitute1,longtitude1,lattitute2,longtitude2,yolId,minlatt,minlong):
        gridlat1,gridlong1 = findGrid(lattitute1, longtitude1, minlatt,minlong)
        gridlat2,gridlong2 = findGrid(lattitute2, longtitude2, minlatt,minlong)
        #assert gridn1 > 0 or gridn2 > 0, "grid1n, grid2n is lt zero {} {},{} {},{} {}".format(gridn1, gridn2,lattitute1,longtitude1,lattitute2,longtitude2)
        coord_yolid_dict[(lattitute1, longtitude1)].append(yolId)
        coord_yolid_dict[(lattitute2, longtitude2)].append(yolId)
        coord_prev_location_dict[(lattitute2, longtitude2)].append((lattitute1, longtitude1))
        coord_gridid_dict[(gridlat1,gridlong1)].append((lattitute1,longtitude1))
        coord_gridid_dict[(gridlat2,gridlong2)].append((lattitute2,longtitude2))
        coord_loc_grid_dict[(lattitute2,longtitude2)].append((gridlat1,gridlong1))
        coord_loc_grid_dict[(lattitute1,longtitude1)].append((gridlat1,gridlong1))


    def ProcessCarData(cardata):
        car_lattitute = float(cardata[0])
        car_longtitute = float(cardata[1])
        car_direction = cardata[2]
        #'G?NEY','KUZEY','KUZEYBATI','DO?U','KUZEYDO?U','BATI','G?NEYDO?U','G?NEYBATI'
        #a car is represented by three points
        carpoint = []
        if car_direction == "G?NEY":
            carpoint.append((car_lattitute - 0.000045,car_longtitute))
            carpoint.append((car_lattitute,car_longtitute))
            carpoint.append((car_lattitute + 0.000045,car_longtitute))
        elif car_direction == "KUZEY":
            carpoint.append((car_lattitute + 0.000045, car_longtitute))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute - 0.000045, car_longtitute))
        elif car_direction == "DO?U":
            carpoint.append((car_lattitute, car_longtitute + 0.000060))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute, car_longtitute - 0.000060))
        elif car_direction == "BATI":
            carpoint.append((car_lattitute, car_longtitute - 0.000060))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute, car_longtitute + 0.000060))
        elif car_direction == "KUZEYDO?U":
            carpoint.append((car_lattitute + 0.000027, car_longtitute + 0.000048))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute - 0.000027, car_longtitute - 0.000048))
        elif car_direction == "KUZEYBATI":
            carpoint.append((car_lattitute + 0.000027, car_longtitute - 0.000048))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute - 0.000027, car_longtitute + 0.000048))
        elif car_direction == "G?NEYDO?U":
            carpoint.append((car_lattitute - 0.000027, car_longtitute + 0.000048))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute + 0.000027, car_longtitute - 0.000048))
        elif car_direction == "G?NEYBATI":
            carpoint.append((car_lattitute - 0.000027, car_longtitute - 0.000048))
            carpoint.append((car_lattitute, car_longtitute))
            carpoint.append((car_lattitute + 0.000027, car_longtitute + 0.000048))
        return carpoint

    def Haversine(tuple1,tuple2):
        #define PI 3.14159265
        #define R 6372795.477598
        PI = 3.14159265
        R = 6372795.477598
        lat1 = float(tuple1[0]) * PI / 180
        lat2 = float(tuple2[0]) * PI / 180
        lon1 = float(tuple1[1]) * PI / 180
        lon2 = tuple2[1] * PI / 180
        dlon = lon2 - lon1;
        dlat = lat2 - lat1;
        a = (math.sin(dlat / 2)) * (math.sin(dlat / 2)) + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)) * (math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d

    def findVals(isX,index,arr,minx,miny,maxx,maxy,prevX,prevY,smallestDistX,smallestDistY,maxDistX,maxDistY):
        if isX:
            global countX
            countX +=1
            arrindex = arr[index]#(arr[index]-29) * 100000
            if minx >= arrindex:
                minx = arrindex
            if maxx <= arrindex:
                maxx = arrindex
            if prevX == None:
                prevX = arrindex
            else:
                #assert abs(prevX-arrindex) > 0, "values of prevX and arr: %f %f %f" % (prevX,arrindex, abs(prevX-arrindex))
                if smallestDistX > (abs(prevX - arrindex)) and abs(prevX - arrindex) != 0:
                    smallestDistX = abs(prevX - arrindex)
                if maxDistX <= (abs(prevX - arrindex)):
                    #print "maxX",prevX,arrindex
                    maxDistX = abs(prevX - arrindex)

        else:
            global countY
            countY += 1
            arrindex = arr[index]#(arr[index]-40) * 100000
            if miny >= arrindex:
                miny = arrindex
            if maxy <= arrindex:
               maxy = arrindex
            if prevY == None:
                prevY = arrindex
            else:
                #assert abs(prevY-arrindex) > 0, "values of prevY and arr: %f %f %f" % (prevY, arrindex, abs(prevY - arrindex))
                if smallestDistY > (abs(prevY - arrindex)) and abs(prevY - arrindex) != 0:
                    smallestDistY = abs(prevY - arrindex)
                if maxDistY <= (abs(prevY - arrindex)):
                    #print "maxY",prevY,arrindex
                    maxDistY = abs(prevY - arrindex)
        return isX,minx,miny,maxx,maxy,prevX,prevY,smallestDistX,smallestDistY,maxDistX,maxDistY

    file = open("newfile.txt", "w")
    countX=0
    countY=0
    strs =""
    minx= sys.float_info.max
    miny =sys.float_info.max
    maxx= 0
    maxy =0
    prevX = None
    prevY =None
    smallestDistX = 10000000
    smallestDistY = 10000000
    maxDistX = 0
    maxDistY = 0
    isX = True
    pointCount=0
    coord_yolid_dict = defaultdict(list)
    coord_prev_location_dict = defaultdict(list)
    coord_gridid_dict = defaultdict(list)
    coord_loc_grid_dict = defaultdict(list)
    callCount = 0
    minLattituteCoord = 4095124 #40
    minLongtitudeCoord = 2901658 #29


    filegrid = open("grids.txt", "w")
    for data_val in data['features']:
        strs=""
        id_yoladi = data_val['properties']['yolAdi']
        strs+=id_yoladi.encode('utf-8')
        strs+=','
        id_yolid = float(data_val['properties']['yolId'])
        strs += "{0:.0f}".format(id_yolid)
        strs += ','
        coord = data_val['geometry']['coordinates']
        if data_val['geometry']['type'] == 'MultiLineString':
            for upper_coord in range(len(coord)):
                for inner_coord in range(3, len(coord[upper_coord]), 4):  ##process two points at a time - 4coords
                    lat1, long1 = coord[upper_coord][inner_coord-2], coord[upper_coord][inner_coord-3]
                    lat2, long2 = coord[upper_coord][inner_coord], coord[upper_coord][inner_coord-1]
                    FillGPSInfo(lat1,long1,lat2,long2,id_yoladi,minLattituteCoord,minLongtitudeCoord)
                    callCount += 1
                if len(coord[upper_coord]) % 4 != 0:
                    #print len(coord[inner_c]) % 4
                    lat1, long1 = coord[upper_coord][-3], coord[upper_coord][-4]
                    lat2, long2 = coord[upper_coord][-1], coord[upper_coord][-2]
                    FillGPSInfo(lat1,long1,lat2,long2,id_yoladi,minLattituteCoord,minLongtitudeCoord)
                    callCount += 1
        else:
            #print len(coord)
            for inner_coord in range(3, len(coord), 4):  ##process two points at a time - 4coords
                lat1, long1 = coord[inner_coord-2],coord[inner_coord-3]
                lat2, long2 = coord[inner_coord], coord[inner_coord-1]
                FillGPSInfo(lat1, long1, lat2, long2, id_yoladi,minLattituteCoord,minLongtitudeCoord)
                callCount += 1
            if len(coord) % 4 != 0:
                lat1, long1 = coord[-3], coord[-4]
                lat2, long2 = coord[-1], coord[-2]
                FillGPSInfo(lat1, long1, lat2, long2, id_yoladi,minLattituteCoord,minLongtitudeCoord)
                callCount += 1
        for inner_c in range(len(coord)):
            if data_val['geometry']['type'] == 'MultiLineString':
                for indexx in xrange(0,len(coord[inner_c])):
                    pointCount +=1
                    isX,minx, miny,maxx,maxy, prevX, prevY, smallestDistX, smallestDistY,maxDistX,maxDistY = findVals(isX,indexx, coord[inner_c], minx, miny,maxx,maxy, prevX, prevY, smallestDistX, smallestDistY,maxDistX,maxDistY)
                    isX = not isX
            else:
                pointCount += 1
                isX,minx, miny,maxx,maxy, prevX, prevY, smallestDistX, smallestDistY,maxDistX,maxDistY = findVals(isX,inner_c, coord, minx, miny,maxx,maxy, prevX, prevY, smallestDistX, smallestDistY,maxDistX,maxDistY)
                isX = not isX
        valll = ','.join(str(item) for item in coord)
        strs += valll #', '.join(str(item) for item in str(coord))
        strs += "\n"
        file.write(strs)
    logging.info("smallestDistX:" + str(smallestDistX))
    logging.info( "smallesDistY:" + str(smallestDistY))
    logging.info( "maxDistX:" + str(maxDistX))
    logging.info( "maxDistY:" + str(maxDistY))
    logging.info( "minX:" + str(minx))
    logging.info( "minY:" + str(miny))
    logging.info( "maxX:" + str(maxx))
    logging.info( "maxY:" + str(maxy))
    logging.info( "No Of points: "+str(pointCount/2))
    logging.info( countX)
    logging.info( countY)
    #logging.info( len(coord_gridid_dict.keys()))
    logging.info( callCount)
    logging.info(coord_loc_grid_dict[(40.98181,29.05821)])
    minElement = 500
    maxElement = 0
    for keys,value in coord_gridid_dict.items():
        if len(coord_gridid_dict[keys]) < minElement:
            minElement = len(coord_gridid_dict[keys])
            logging.info("min keys:" + str(keys) + " " + str(minElement))
        if len(coord_gridid_dict[keys]) > maxElement:
            maxElement = len(coord_gridid_dict[keys])
            logging.info("max keys:" + str(keys) + " " + str(maxElement))
    logging.info(minElement)
    logging.info(maxElement)
    logging.info(coord_gridid_dict.keys())
    logging.info(coord_gridid_dict[5])

print "reading csv data..."
Directions = ['G?NEY','KUZEY','KUZEYBATI','DO?U','KUZEYDO?U','BATI','G?NEYDO?U','G?NEYBATI']

#lattitute +-90 is 10m
#longtitute +-12 is 10m

csv_link = "/Users/gorkeralp/Dropbox/Okul/Research/QPU/gps_data_csv/gps data1.csv"
with open(csv_link) as f:
    car_gps_points = csv.reader(f)
    for gps_point in car_gps_points:
        break; #pass the initial row for signatures
    for gps_point in car_gps_points:
        car_data = [gps_point[5],gps_point[6],gps_point[9]] #lattitute,longtitude,direction
        #first tuple point is where the car is headed
        #second tuple point is the actual gps data
        #third tuple point is the rear point
        FindNearestPointInMap(car_data)


        #gridn1, hashedCoord1 = findGrid(lat1, long1, 13, 13027)

        #findGrid(processed_car_data[0])
        ##post processing based on direction and accuracy


