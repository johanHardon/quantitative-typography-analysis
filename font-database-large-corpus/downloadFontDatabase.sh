#!/bin/bash

letters="Hpkxoa Hp pk kx xo oa H p k x o a"
while IFS=";" read -r category family stylename styleid; do
	python3 allFontsForCategoryApi.py -c "$category" -f "$family" -s "$stylename" -i "$styleid"  -l "$letters"
done < <(tail -n +2 $1) #Ignores header line

