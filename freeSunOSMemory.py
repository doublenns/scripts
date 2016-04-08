#!/usr/bin/env python
import subprocess
import csv

'''
Script grabs SunOS memory statistics and outputs as CSV
To Do
* Free Memory Percentage
* Memory Paging PiT
* Memory Activity Page Scan PiT
'''

def run_shell_command(cmd, *shell):
	# Might want to use a "try" or call.check in case bashCommand fails
	# i.e. not a SunOS box
	bash_command = cmd
	if "shell" in shell:
		process = subprocess.Popen(cmd,
			stdout=subprocess.PIPE, shell=True)
	else:
		process = subprocess.Popen(cmd.split(),
			stdout=subprocess.PIPE)
	output = process.communicate()[0]
	return output


# Use the second line of vmstat output as Free Memory Statistics
free_memory_statistics = run_shell_command("vmstat 1 2").split('\n')[3]
free_memory = free_memory_statistics.split()[4]
total_memory_statistics = run_shell_command("prtconf | grep Memory", "shell")
total_memory = total_memory_statistics.split(":")[1].strip()

csv_file = open('memoryUtilization.csv', 'w')
writer = csv.writer(csv_file)
data = [
	['Name', 'Value'],
	['Free Memory', free_memory],
	['Total Memory', total_memory]
]
writer.writerows(data)
csv_file.close()



# 'prtconf | grep Memory' cmd gives total SunOS system memory
# 'kstat -n system_pages' cmd gives some other memory statistics
