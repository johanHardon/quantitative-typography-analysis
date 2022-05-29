#!/bin/bash

function endsWithNewline() {
	[[ $(tail -c1 "$1" | wc -l) -gt 0 ]]
}

#Adds newline if not already there (i.e. if has been saved in excel)
if ! endsWithNewline "$1"
then
	echo "" >> "$1"
fi

for filename in ../font-database/database/script/*/*/one-letter/*.png; do
	python3 orientationExpansion.py -i "$filename" -o "$1"
done
