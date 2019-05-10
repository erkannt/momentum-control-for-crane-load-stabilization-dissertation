#!/bin/sh

for f in robot-toolpaths-*; do
  duration=$(ffprobe -v error -show_streams $f | grep duration= | cut -f2 -d =)
  ffmpeg -y -i $f -filter:v "setpts=(20/$duration)*PTS" ${f/%.mov/-tmp.mp4}
  ffmpeg -y -i ${f/%.mov/-tmp.mp4} -vf crop=in_w/2.7:in_h/1.2:in_w/1.8:in_h/2-out_h/2 ${f/%.mov/-cropped.mp4} 
done

ffmpeg -y \
  -i robot-toolpaths-1-cropped.mp4 \
  -i robot-toolpaths-2-cropped.mp4 \
  -i robot-toolpaths-3-cropped.mp4 \
  -filter_complex hstack=inputs=3 \
  stacked.mp4

ffmpeg -y -i stacked.mp4 -vf crop=in_w/1.1:in_h:0:in_w/2 robot-toolpaths.mp4

