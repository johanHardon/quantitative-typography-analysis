#!/bin/bash

function endsWithNewline() {
  [[ $(tail -c1 "$1" | wc -l) -gt 0 ]]
}

#Adds newline if not already there (i.e. if has been saved in excel)
if ! endsWithNewline "$1"
then
  echo "" >> "$1"
fi

fontSample="Hpkxoa"
while IFS=";" read -r font style category; do
		python3 HpkxoaLetterApi.py -f "$font" -s "$style" -c "$category"  -l "$fontSample"
done < <(tail -n +2 $1) #Ignores header line

