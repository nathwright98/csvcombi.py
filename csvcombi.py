# -*- coding: utf-8 -*-
"""
csvcombi.py: Combines data in CSV files according to user-defined preferences.
Copyright(C) 2020 Nathan C. Wright

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
import csv
import statistics as stats
import os
import time
"""
Takes comma-separated variable files and combines entries in the files according to user-selected parameters.
"""
#This corresponds to the filename of the input CSV file
inputName = 'input.csv'
#This corresponds to the column containing the ID values by which data entries can be combined
combineColumn = 0
#Column functions should be placed in this list
colFunctions = [
    [1, 'MEAN'],
    [2, 'MEAN'],
    [3, 'MEAB']
    ]
#This corresponds to the filename of the output CSV file
outputName = 'output.csv'

class DataEntry:
    """
    Represents a reduced data entry with all relevant data combined
    """
    #Data ID identifies the data entry
    dataID = None
    #Corresponds to all data which is associated with this entry
    dataLists = []
    
    def __init__(self, dataID, functions):
        self.dataID = dataID
        self.dataLists = []
        #For each column which is to be kept in the reduced CSV, instantiate a blank list
        for i in range(functions):
            self.dataLists.append([])
            
def getCFString(cf):
    """
    Returns a string describing the calculation performed on values in a column.
    """
    if(cf[1] == 'MAX'):
        return('Maximum value selected for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'MEAN'):
        return('Average value calculated for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'MEDIAN'):
        return('Median value calculated for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'MIN'):
        return('Minimum value selected for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'MODE'):
        return('Most common value calculated for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'STDEV'):
        return('Standard deviation calculated for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'SUM'):
        return('Sum of values calculated for column ' + str(cf[0]) + '.')
    elif(cf[1] == 'VAR'):
        return('Variance calculated for column ' + str(cf[0]) + '.')
    #If the function type was not valid, return this specific message.
    else:
        return('Average value calculated for column ' + str(cf[0]) + '. This calculation was performed as a fallback due to an incorrect entry in the column functions list.')

#Create a list for new data entries
dataEntries = []
#Create a counter for entries which could not be parsed
unparsed = 0
unparsedData = []

#Track number of lines, also used for iterating over lines
lineCount = 0

#Track whether an incorrect function was entered
badFunctionWarning = False

#Record start time of main body
startTime = time.time()

#Open the input CSV file
with open(inputName) as csvFile:
    csvReader = csv.reader(csvFile, delimiter = ',')
    
    #Iterate through each row of the CSV file
    for row in csvReader:
        #Ignore first line as this corresponds to column titles, otherwise iterate through each row of data
        if lineCount > 0:
            #Check that a data entry does not already exist for data with the same ID as this row
            if not any(data.dataID == row[combineColumn] for data in dataEntries):
                #Create a new data entry with an ID corresponding to this row
                dataEntries.append(DataEntry(row[combineColumn], len(colFunctions)))
            #Get the data entry corresponding to the ID of this row
            d = next(data for data in dataEntries if (data.dataID == row[combineColumn]))
            
            #For each column which should be recorded to it, add the data contained in this row
            for r in range(len(colFunctions)):
                #Try to parse value as float
                try:
                    d.dataLists[r].append(float(row[colFunctions[r][0]]))
                #If not possible, increment unparsed data counter and log unparsed data value and location
                except:
                    unparsed += 1
                    unparsedData.append([row[colFunctions[r][0]], lineCount, r])
        #Increment the line count
        lineCount += 1

#Create a list to contain data that should be written to the output CSV
dataToWrite = []
        
#Iterate through data entries
for d in dataEntries:
    #Create a list of condensed data, with the data ID as the first column value
    dataToStore = [d.dataID]
    #Iterate through all data assocaited with this data entry, and apply functions to columns as necessary to condense the data
    for dList in range(len(d.dataLists)):
        if colFunctions[dList][1] == 'MAX':
            dataToStore.append(max(d.dataList[dList]))
        elif colFunctions[dList][1] == 'MEAN':
            dataToStore.append(stats.mean(d.dataLists[dList]))
        elif colFunctions[dList][1] == 'MEDIAN':
            dataToStore.append(stats.median(d.dataList[dList]))
        elif colFunctions[dList][1] == 'MIN':
            dataToStore.append(min(d.dataList[dList]))
        elif colFunctions[dList][1] == 'MODE':
            dataToStore.append(stats.mode(d.dataList[dList]))
        elif colFunctions[dList][1] == 'STDEV':
            dataToStore.append(stats.stdev(d.dataList[dList]))
        elif colFunctions[dList][1] == 'SUM':
            dataToStore.append(sum(d.dataList[dList]))
        elif colFunctions[dList][1] == 'VAR':
            dataToStore.append(stats.variance(d.dataList[dList]))
        else:
            dataToStore.append(stats.mean(d.dataLists[dList]))
            badFunctionWarning = True
    #Add this condensed data entry to the list of data to write
    dataToWrite.append(dataToStore)
    
#Create an output CSV and write the data to it
with open(outputName, 'w+', newline='') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter = ',')
    for d in dataToWrite:
        csvWriter.writerow(d)

#Calculate duration of main body
endTime = time.time() - startTime

#Provide information regarding output file location
print('Output CSV file saved to ' + os.getcwd() + '\\' + outputName + '.')
logtext = 'Output CSV file saved to ' + os.getcwd() + '\\' + outputName + '.'

#Provide information on how the CSV was reduced and the duration of the reduction process
print('CSV reduced from ' + str(lineCount) + ' entries to ' + str(len(dataEntries)) + ' entries in ' + str(endTime) + ' seconds.')
logtext += '\n\nCSV reduced from ' + str(lineCount) + ' entries to ' + str(len(dataEntries)) + ' entries in ' + str(endTime) + ' seconds.\nThe data was reduced using the following methods:'
for cf in colFunctions:
    logtext += '\n' + getCFString(cf)

#Display a warning if an incorrect column function was entered
if(badFunctionWarning == True):
    print('\nAn incorrect column function was passed to the script. The mean function was applied as a fallback, however this may not have been your intention. Your data may be incorrect as a result. Please check your column function syntax for any mistakes.')    
    logtext += '\n\nAn incorrect column function was passed to the script. The mean function was applied as a fallback, however this may not have been your intention. Your data may be incorrect as a result. Please check your column function syntax for any mistakes.'

#Display information about any unparsed entries
if(unparsed > 0):
    print(str(unparsed) + ' data entries could not be parsed and have not been accounted for. More data is available in the log file.')
    logtext += '\n\n' + str(unparsed) + ' data entries could not be parsed and have not been accounted for.\nA list of unparsed data entries is as follows:'
    for entry in unparsedData:
        logtext += '\nEntry \'' + str(entry[0]) + '\' in row ' + str(entry[1]) + ', column ' + str(entry[2]) + '.'
#If no unparsed entries exist, log this information 
else:
    logtext += '\n\nAll entries in selected columns were parsed successfully.'

#Write logs to a .txt file
textFile = open('log.txt', 'w')
textFile.write(logtext)
textFile.close()