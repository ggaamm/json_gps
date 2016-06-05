import json
import sys
from collections import defaultdict
import logging

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
    maxValHashed=0

    def findGrid(lattitude,longtitude,shiftn,value):
        ll = (lattitude << shiftn)+long(longtitude)
        gridnumber = ll / value #corresponds to value
        #gridnum = long(ll / 2**grids)
        return long(gridnumber),long(ll)

    def NormalizeCoord(lattitude,longtitude,minlattitude,minlongtitude):
        decPointLat = (lattitude*100000) - minlattitude
        decPointLong = (longtitude*100000) - minlongtitude
        return (long(decPointLat),long(decPointLong))

    def FillGPSInfo(latt1,longg1,latt2,longg2,yolId,minlatt,minlong):
        global maxValHashed
        lat1, long1 = NormalizeCoord(latt1,longg1,minlatt,minlong)
        lat2, long2 = NormalizeCoord(latt2,longg2,minlatt,minlong)
        assert lat1 > 0 or long1 > 0,  "lat1, long1 is lt zero {} {}".format(lat1, long1)
        assert lat2 > 0 or long2 > 0, "lat2, long2 is lt zero {} {}".format(lat2, long2)
        gridn1, hashedCoord1 = findGrid(lat1, long1, 13, 13027)
        gridn2, hashedCoord2 = findGrid(lat2, long2, 13, 13027)
        assert gridn1 > 0 or gridn2 > 0, "grid1n, grid2n is lt zero {} {},{} {},{} {}".format(gridn1, gridn2,latt1,longg1,latt2,longg2)
        coord_yolid_dict[(latt1, longg1)].append(yolId)
        coord_yolid_dict[(latt2, longg2)].append(yolId)
        coord_prev_location_dict[(latt2, longg2)].append((latt1, longg1))
        coord_gridid_dict[gridn1].append((latt1,longg1))
        coord_gridid_dict[gridn2].append((latt2,longg2))

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
    callCount = 0
    minLattituteCoord = 4095124 #40
    maxLongtitudeCoord = 2901658 #29

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
                    FillGPSInfo(lat1,long1,lat2,long2,id_yolid,minLattituteCoord,maxLongtitudeCoord)
                    callCount += 1
                if len(coord[upper_coord]) % 4 != 0:
                    #print len(coord[inner_c]) % 4
                    lat1, long1 = coord[upper_coord][-3], coord[upper_coord][-4]
                    lat2, long2 = coord[upper_coord][-1], coord[upper_coord][-2]
                    FillGPSInfo(lat1,long1,lat2,long2,id_yolid,minLattituteCoord,maxLongtitudeCoord)
                    callCount += 1
        else:
            #print len(coord)
            for inner_coord in range(3, len(coord), 4):  ##process two points at a time - 4coords
                lat1, long1 = coord[inner_coord-2],coord[inner_coord-3]
                lat2, long2 = coord[inner_coord], coord[inner_coord-1]
                FillGPSInfo(lat1, long1, lat2, long2, id_yolid,minLattituteCoord,maxLongtitudeCoord)
                callCount += 1
            if len(coord) % 4 != 0:
                lat1, long1 = coord[-3], coord[-4]
                lat2, long2 = coord[-1], coord[-2]
                FillGPSInfo(lat1, long1, lat2, long2, id_yolid,minLattituteCoord,maxLongtitudeCoord)
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
        valll = ', '.join(str(item) for item in coord)
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
    logging.info( len(coord_gridid_dict.keys()))
    logging.info( callCount)
    logging.info( maxValHashed)
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

