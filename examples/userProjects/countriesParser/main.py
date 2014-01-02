from weioLib.weioUserApi import attach
import json

def setup():
    attach.process(myProcess)
    
def myProcess():
    f = open("countries.csv", "r")
    countryList = []
    a = 0
    for line in f:
        #print line
        splittedLine = line.split(",")
        countryName = splittedLine[0]
        countrySymbol = splittedLine[2]
        countryList.append([countryName,countrySymbol])
        
        print countryList[a]
        a+=1
        
    del(countryList[0])
    
    inputFile = open("countries.txt", 'w')
    #print(inputFile)
    ret = inputFile.write(json.dumps(countryList, sort_keys=True))
    inputFile.close()
    