import json
import sys
import re
from pprint import pprint

# -*- coding: utf-8 -*-
with open("/home/alp/Dropbox/Okul/Research/QPU/kadikoy_yol.json") as data_file:
    data = json.load(data_file)
    #print type(data)
    #print len(data)
    #print data.keys()
    #print (data)
    #print type(coord)
    print('------')
    countX=0
    countY=0

    def findGrid(latti,longi,shiftn,grids):
        ll = (latti * 2**shiftn)+long(longi)
        ll /= 52113
        #gridnum = long(ll / 2**grids)
        return long(ll)

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
                    print "maxX",prevX,arrindex
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
                    print "maxY",prevY,arrindex
                    maxDistY = abs(prevY - arrindex)
        return isX,minx,miny,maxx,maxy,prevX,prevY,smallestDistX,smallestDistY,maxDistX,maxDistY

    file = open("newfile.txt", "w")
    countX =0
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

    filegrid = open("grids.txt", "w")
    for data_val in data['features']:
        strs=""
        ids = data_val['properties']['yolAdi']
        strs+=ids.encode('utf-8')
        strs+=','
        ids = float(data_val['properties']['yolId'])
        strs += "{0:.0f}".format(ids)
        strs += ','
        coord = data_val['geometry']['coordinates']
        for inner_c in range(0,len(coord),2):
            if data_val['geometry']['type'] == 'MultiLineString':
                for indexx in xrange(0, len(coord[inner_c]),2):
                    longg = float((coord[inner_c][indexx] * 100000) - 2901658)
                    latt = float((coord[inner_c][indexx+1] * 100000) - 4095124)
                    gridn= findGrid(latt, longg,13,10)
                    filegrid.write(str(gridn)+"\n")

            else:
                longg = float((coord[inner_c] * 100000) - 2901658)
                latt = float((coord[inner_c+1] * 100000) - 4095124)
                gridn = findGrid(latt, longg, 13, 10)
                filegrid.write(str(gridn) + "\n")

        for inner_c in range(len(coord)):
            #print inner_c
            if data_val['geometry']['type'] == 'MultiLineString':
                #print data_val['geometry']['type']
                #print data_val['properties']['yolAdi']
                for indexx in xrange(0,len(coord[inner_c])):
                    pointCount +=1
                    #print indexx
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

        #pprint (strs)

    print "smallestDistX:" + str(smallestDistX)
    print "smallesDistY:" + str(smallestDistY)
    print "maxDistX:" + str(maxDistX)
    print "maxDistY:" + str(maxDistY)
    print "minX:" + str(minx)
    print "minY:" + str(miny)
    print "maxX:" + str(maxx)
    print "maxY:" + str(maxy)
    print "No Of points: "+str(pointCount/2)
    print countX
    print countY
