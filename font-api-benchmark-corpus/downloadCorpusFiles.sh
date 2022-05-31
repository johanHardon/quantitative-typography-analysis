#!/bin/bash

function endsWithNewline() {
	[[ $(tail -c1 "$1" | wc -l) -gt 0 ]]
}

#Adds newline if not already there (i.e. if has been saved in excel)
if ! endsWithNewline "$1"
then
	echo "" >> "$1"
fi

letters="Hpkxoa"
while IFS=";" read -r font style category; do
	for ((i=0;i<${#letters};i++)); do
		#python3 letterApi.py -f "$font" -s "$style" -c "$category"  -l "${letters:$i:1}"
		echo "$font"
	done
done < <(tail -n +2 $1) #Ignores header line

