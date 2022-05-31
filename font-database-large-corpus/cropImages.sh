#!/bin/bash

for filename in $1/sans-serif/*/*/*/*k.png; do
	python3 crop.py -i "$filename"
done
