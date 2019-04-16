#!/bin/sh
# Convert all mp4 in data to gif, copy to figures
#
# Requires [gifify](https://github.com/vvo/gifify)
# Only converts if gif doesn't already exist.
for f in $(find ./data -name "*.mp4"); do
    if [ ! -f ${f/%.mp4/.gif} ]; then
          echo $f
              gifify $f --resize '800:-1' -o ${f/%.mp4/.gif}
                fi
                  cp ${f/%.mp4/.gif} ./figures/
                done
