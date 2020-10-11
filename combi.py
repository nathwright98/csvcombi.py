# -*- coding: utf-8 -*-
import csv

"""
ENTER DESIRED COLUMN FUNCTIONS IN THIS LIST
"""
colFunctions = [
    ]

class DataEntry:
    dataID = None
    dataLists = []
    
    def __init__(self, dataID, functions):
        self.dataID = dataID
        self.dataLists = []
        for i in range(functions):
            self.dataLists.append([])

combineRow = 0

dataEntries = []

with open('input.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter = ',')
    lineCount = 0
    
    for row in csvReader:
        #Ignore first line as this corresponds to column titles, otherwise iterate through each row of data
        if lineCount > 0:
            if not any(data.dataID == row[0] for data in dataEntries):
                dataEntries.append(DataEntry(row[0], len(colFunctions)))
            d = next(data for data in dataEntries if (data.dataID == row[0]))
 
            for r in range(len(colFunctions)):
                d.dataLists[r].append(float(row[colFunctions[r][0]]))
            
        lineCount += 1

dataToWrite = []
        
for d in dataEntries:
    dataToStore = [d.dataID]
    for dList in range(len(d.dataLists)):
        if colFunctions[dList][1] == 'AVERAGE':
            dataToStore.append(sum(d.dataLists[dList])/len(d.dataLists[dList]))
    dataToWrite.append(dataToStore)
    
with open('output.csv', 'w+', newline='') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter = ',')
    for d in dataToWrite:
        csvWriter.writerow(d)
    