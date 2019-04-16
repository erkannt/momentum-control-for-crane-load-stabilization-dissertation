#!/bin/sh

for f in $(find ./data -name "*.py"); do
python $f
done

for f in $(find ./figures -name "*.svg"); do
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i "" 's/width.*pt\"//g' $f
    sed -i "" 's/height.*pt\"//g' $f
  else
    sed -i 's/width.*pt\"//g' $f
    sed -i 's/height.*pt\"//g' $f
  fi
done