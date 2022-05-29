#!/bin/bash

function endsWithNewline() {
	[[ $(tail -c1 "$1" | wc -l) -gt 0 ]]
}

#Adds newline if not already there (i.e. if has been saved in excel)
if ! endsWithNewline "$1"
then
	echo "" >> "$1"
fi


# for file in  ../font-database/database/Hand/*/*/one-letter/*.png; do
# 	python3 curvature.py -i "$file" -o "$1" --maxcorner1 4 --maxcorner2 5 --drawstraight 40 -s 170
# done

for file in  ../font-database/database/sans-serif/*/*/one-letter/*.png; do
	python3 curvature.py -i "$file" -o "$1" --maxcorner1 4 --maxcorner2 50 --drawstraight 40 -s 170
done

# for file in  ../font-database/database/script/*/*/one-letter/*.png; do
# 	python3 curvature.py -i "$file" -o "$1" --maxcorner1 4 --maxcorner2 0 --drawstraight 40 -s 175 
# done

# for file in  ../font-database/database/serif/*/*/one-letter/*.png; do
# 	python3 curvature.py -i "$file" -o "$1" --maxcorner1 4 --maxcorner2 30 --drawstraight 40 -s 175
# done


# for file in  ../font-database/database/slab-serif/*/*/one-letter/*.png; do
# 	python3 curvature.py -i "$file" -o "$1" --maxcorner1 4 --maxcorner2 30 --drawstraight 40 -s 170
# done

# for file in  ../font-database/database/slab-serif/*/*/one-letter/*.png; do
	# python3 curvature.py -i "$file" -o "$1" --maxcorner1 4 --maxcorner2 30 --drawstraight 40 -s 170
# done
# 





#for file in  ../all-assets/corpus-images/Script/*/one-letter/*.png; do
#	#echo "$file"
#	python3 yorkStack.py -i "$file" -o "$1" 
#
#done
