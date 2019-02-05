#!/bin/sh

for f in $(find ./data -name "*.py"); do
python $f
done