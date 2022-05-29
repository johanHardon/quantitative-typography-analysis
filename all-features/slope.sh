#!/bin/bash

function endsWithNewline() {
	[[ $(tail -c1 "$1" | wc -l) -gt 0 ]]
}

#Adds newline if not already there (i.e. if has been saved in excel)
if ! endsWithNewline "$1"
then
	echo "" >> "$1"
fi

for file in ../font-database/database/serif/*/*/one-letter/*k.png; do
	python3 slope.py -i "$file" -o "$1" 
done

