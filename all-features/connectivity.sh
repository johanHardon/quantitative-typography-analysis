#!/bin/bash

function endsWithNewline() {
 	[[ $(tail -c1 "$1" | wc -l) -gt 0 ]]
 }

#Adds newline if not already there (i.e. if has been saved in excel)
 if ! endsWithNewline "$1"
 then
 	echo "" >> "$1"
fi
declare -a array=()
for filename in ../font-database/database/serif/*/*/two-letter/*.png;do
	item=$filename
	array+=($item)
	
	if [ ${#array[@]} -eq 5 ]
	then
   		python3 connectivity.py -i "${array[@]}" -o "$1"
    	unset array
	fi
done
