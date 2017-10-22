#!/bin/bash -

FREE_MEMORY=$(vmstat 1 2 | sed -n '$p' | awk '{print $5}')
TOTAL_MEMORY_MB=$(prtconf | grep Memory | awk '{print $3}')
TOTAL_MEMORY=$(($TOTAL_MEMORY_MB * 1024))
FREE_MEMORY_PERC=$(( ($FREE_MEMORY * 100) / $TOTAL_MEMORY ))

CSV_FILE="memoryUtilization.csv"

echo "Name, Value" > "$CSV_FILE"
echo "Total Memory, $TOTAL_MEMORY" >> "$CSV_FILE"
echo "Free Memory, $FREE_MEMORY" >> "$CSV_FILE"
echo "Free Memory%, $FREE_MEMORY_PERC" >> "$CSV_FILE"

cat "$CSV_FILE"

