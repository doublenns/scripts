#!/bin/bash -

# Script grabs contents of /etc/vfstab and outputs to CSV

CSV_FILE=mount_output.csv
HEADER="Device to Mount, Device to fsck, Mount Point, FS Type, fsck Pass, \
	Mount at Boot, Mount Options"

# Not quoting HEADER because don't want to include leading whitespace on second line
echo $HEADER > "$CSV_FILE"
cat /etc/vfstab | sed 's/,/;/g' | sed -e 's/^#.*//' -e '/^$/d' |\
	grep -v swap | >> "$CSV_FILE"
cat "$CSV_FILE"
