'''
Created on 04.04.2013

@author: ActionLuzifer
'''
import os
import re

class Month(object):
    
    def __init__(self, year, month):
        self.month = month
        self.year = year
        self.sender = []




regex = "(?P<SENDUNG>(.*))_(?P<YEAR>(\d\d))\.(?P<MONTH>(\d\d))\.(?P<DAY>(\d\d))_(?P<HOUR>(\d\d))-(?P<MIN>(\d\d))_(?P<SENDER>(.*))_(?P<LENGTH>((\d)*))_TVOON_DE.(?P<FORMAT>(.*))"
regexProgramm = re.compile(regex)

def getData(_filename):
    foundRE = regexProgramm.search(_filename)
    isAnOTVFile = True
    if foundRE:
        sendung  = foundRE.group("SENDUNG")
        year     = foundRE.group("YEAR")
        month    = foundRE.group("MONTH")
        day      = foundRE.group("DAY")
        hour     = foundRE.group("HOUR")
        min      = foundRE.group("MIN")
        sender   = foundRE.group("SENDER")
        length   = foundRE.group("LENGTH")
        format   = foundRE.group("FORMAT")
    else:
        isAnOTVFile = False
        year    = "00"
        month   = "00"
        sender  = "unknown"
        
    return year, month, sender, isAnOTVFile


def getObj(liste, inhalt, toDict=True):
    wanted = liste.get(inhalt)
    if wanted:
        pass
    else:
        if toDict:
            wanted = {}
        else:
            wanted = []
        liste[inhalt]=wanted
    return wanted


def checkForPath(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def loadDescription():
    description = {}
    descfilename = os.path.normpath("descript.ion")
    if os.path.exists(descfilename):
        descriptionFile = open(descfilename, "r")
        sstr = descriptionFile.readline().lstrip().rstrip()
        while sstr != "":
            if sstr[0] == '"':
                stelle = sstr.find('"',2)
                print("#"+sstr[1:stelle]+"### -> ###"+sstr[stelle+2:]+"#")
                description[sstr[1:stelle]] = sstr[stelle+2:]
            else:
                stelle = sstr.find(" ",2)
                description[sstr[:stelle]] = sstr[stelle+1:]
    
            sstr = descriptionFile.readline().lstrip().rstrip()
        descriptionFile.close()
    return description


def writeDescription(_path, _filename, _description):
    descfilename = os.path.normpath(_path+"/descript.ion")
    descriptionFile = open(descfilename, "a")
    if " " in _filename:
        line = '"'+_filename+'" '+_description
    else:
        line = ''+_filename+' '+_description
    descriptionFile.write(line+"\r\n")
    descriptionFile.close()


if __name__ == '__main__':
    years = {}
    files = os.listdir(".")
    descriptionDict = loadDescription()
    for file in files:
        if os.path.isfile(file):
            year, month, sender, isAnOTVFile = getData(file)
            if isAnOTVFile:
                #print("Y: "+year+" | M: "+month+" | S: "+sender+" | "+file)
                yearO   = getObj(years,year)
                monthO  = getObj(yearO,month)
                senderO = getObj(monthO,sender, False)
                senderO.append(file)


    for y in years.items():
        print("YEAR: "+str(y[0]))
        for m in y[1].items():
            print("      MON: "+str(m[0]))
            for s in m[1].items():
                print("          sender: "+str(s[0]))
                path = os.path.normpath(str(y[0])+"-"+str(m[0])+"/"+"/"+str(s[0]))
                checkForPath(path)
                print(path)
                for filename in s[1]:
                    if filename in descriptionDict:
                        description = descriptionDict[filename]
                        print("                    #"+str(filename)+"#")
                        print("                   ->"+description)
                        writeDescription(path, filename, description)
                    os.renames(filename, os.path.normpath(path+"/"+filename))
