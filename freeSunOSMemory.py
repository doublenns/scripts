#!/usr/bin/env python
import subprocess
import csv

'''
Script grabs SunOS memory statistics and outputs as CSV
To Do
* Memmory Paging PiT
* Memory Activity Page Scan PiT
'''

bashCommand = "vmstat 1 2"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# Might want to use a "try" or call.check in case bashCommand fails
# i.e. not a SunOS box
output = process.communicate()[0]
# Use the second line of cmd output as Memory Statistics
memoryStatistics = output.split('\n')[3]
freeMemory = memoryStatistics.split()[4]

csvFile = open('memoryUtilization.csv', 'w')
writer = csv.writer(csvFile)

data = [
	['Total Memory', freeMemory],
	['Free Memory', freeMemory]
]

writer.writerows(data)
csvFile.close()

exit(0)



# 'prtconf | grep Memory' cmd gives total SunOS system memory
