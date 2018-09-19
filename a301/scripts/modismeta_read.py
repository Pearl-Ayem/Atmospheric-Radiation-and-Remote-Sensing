"""
  a301.scripts.modismeta_read 
  ________________________

  parses a Modis Level1b CoreMetata.0 string and extracts
  a dictionary. 

  to run from the command line::

    python -m a301.scripts.modismeta_read  level1b_file.hdf

  to run from a python script::

    from a301.scripts.modismeta_read import parseMeta
    out=parseMeta(hdf_file)
"""
from __future__ import print_function

import types
import numpy as np
import argparse
from pathlib import Path
from pyhdf.SD import SD, SDC
import sys
import pprint

class metaParse:
    def __init__(self,metaDat):
        import re
        self.metaDat=str(metaDat).rstrip(' \t\r\n\0')
        #search for the string following the words "VALUE= "
        self.stringObject=\
             re.compile('.*VALUE\s+=\s"(?P<value>.*)"',re.DOTALL)
        #search for a string that looks like 11:22:33
        self.timeObject=\
             re.compile('.*(?P<time>\d{2}\:\d{2}\:\d{2}).*',re.DOTALL)
        #search for a string that looks like 2006-10-02
        self.dateObject=\
             re.compile('.*(?P<date>\d{4}-\d{2}-\d{2}).*',\
                        re.DOTALL)
        #search for a string that looks like "(anything between parens)"
        self.coordObject=re.compile('.*\((?P<coord>.*)\)',re.DOTALL)
        #search for a string that looks like "1234"
        self.orbitObject=\
             re.compile('.*VALUE\s+=\s(?P<orbit>\d+)\n',re.DOTALL)

    def getstring(self,theName):
        theString=self.metaDat.split(theName)
        theString = [str(item) for item in theString]
        #should break into three pieces, we want middle
        out=[item[:50] for item in theString]
        if len(theString) ==3:
            theString=theString[1]
        return theString
        

    def __call__(self,theName):
        if theName=='CORNERS':
            import string
            #look for the corner coordinates by searching for
            #the GRINGPOINTLATITUDE and GRINGPOINTLONGITUDE keywords
            #and then matching the values inside two round parenthesis
            #using the coord regular expression
            theString= self.getstring('GRINGPOINTLATITUDE')
            theMatch=self.coordObject.match(theString)
            theLats=theMatch.group('coord').split(',')
            theLats=[float(item) for item in theLats]
            theString= self.getstring('GRINGPOINTLONGITUDE')
            theMatch=self.coordObject.match(theString)
            theLongs=theMatch.group('coord').split(',')
            theLongs=[float(item) for item in theLongs]
            lon_list,lat_list = np.array(theLongs),np.array(theLats)
            min_lat,max_lat=np.min(lat_list),np.max(lat_list)
            min_lon,max_lon=np.min(lon_list),np.max(lon_list)
            lon_0 = (max_lon + min_lon)/2.
            lat_0 = (max_lat + min_lat)/2.
            corner_dict = dict(lon_list=lon_list,lat_list=lat_list,
                               min_lat=min_lat,max_lat=max_lat,min_lon=min_lon,
                               max_lon=max_lon,lon_0=lon_0,lat_0=lat_0)
            value=corner_dict
        #regular value
        else:
            theString= self.getstring(theName)
            #orbitnumber doesn't have quotes
            if theName=='ORBITNUMBER':
                theMatch=self.orbitObject.match(theString)
                if theMatch:
                    value=theMatch.group('orbit')
                else:
                    raise Exception("couldn't fine ORBITNUMBER")
            #expect quotes around anything else:
            else:
                theMatch=self.stringObject.match(theString)
                if theMatch:
                    value=theMatch.group('value')
                    theDate=self.dateObject.match(value)
                    if theDate:
                        value=theDate.group('date') + " UCT"
                    else:
                        theTime=self.timeObject.match(value)
                        if theTime:
                            value=theTime.group('time') + " UCT"
                else:
                    raise Exception("couldn't parse %s" % (theName,))
        return value

def parseMeta(filename):
    """
    Read useful information from a CoreMetata.0 attribute

    Parameters
    ----------

    filename: str or Path object
       name of an hdf4 modis level1b file

    Returns
    -------
    
    outDict: dict
        key, value:

    lat_list: np.array
        4 corner latitudes
    lon_list: np.array
        4 corner longitudes
    max_lat: float
        largest corner latitude
    min_lat: float
        smallest corner latitude
    max_lon: float
        largest corner longitude
    min_lon: float
        smallest corner longitude
    daynight: str
        'Day' or 'Night'
    starttime: str
        swath start time in UCT
    stoptime: str
        swath stop time in UCT
    startdate: str
        swath start datein UCT
    orbit: str
        orbit number
    equatordate: str
        equator crossing date in UCT
    equatortime: str
        equator crossing time in UCT
    nasaProductionDate: str
        date file was produced, in UCT
    """
    filename=str(filename)
   
    the_file = SD(filename, SDC.READ)
    metaDat=the_file.attributes()['CoreMetadata.0']

    parseIt=metaParse(metaDat)
    outDict={}
    outDict['orbit']=parseIt('ORBITNUMBER')
    outDict['filename']=parseIt('LOCALGRANULEID')
    outDict['stopdate']=parseIt('RANGEENDINGDATE')
    outDict['startdate']=parseIt('RANGEBEGINNINGDATE')
    outDict['starttime']=parseIt('RANGEBEGINNINGTIME')
    outDict['stoptime']=parseIt('RANGEENDINGTIME')
    outDict['equatortime']=parseIt('EQUATORCROSSINGTIME')
    outDict['equatordate']=parseIt('EQUATORCROSSINGDATE')
    outDict['nasaProductionDate']=parseIt('PRODUCTIONDATETIME')
    outDict['daynight']=parseIt('DAYNIGHTFLAG')
    corners=parseIt('CORNERS')
    outDict.update(corners)
    return outDict

def make_parser():
    """
    set up the command line arguments needed to call the program
    """
    linebreaks = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=linebreaks, description=__doc__.lstrip())
    parser.add_argument('h4_file', type=str, help='name of h4 file')
    return parser

def main(args=None):
    """
    args: optional -- if missing then args will be taken from command line
          or pass [h4_file] -- list with name of h4_file to open
    """
    parser = make_parser()
    parsed_args = parser.parse_args(args)
    filename = str(Path(parsed_args.h4_file).resolve())
    out=parseMeta(filename)
    pprint.pprint(out)

if __name__=='__main__':
    sys.exit(main())

