#!/bin/sh

for f in *nms.mp4; do
  ffmpeg -y -i $f -vf crop=1060:1200:in_w/2-out_w/2+40:in_h/2-out_h/2-100 ${f/%.mp4/-cropped.mp4}
done
ffmpeg -y \
  -i h-max-25-nms-cropped.mp4 \
  -i h-max-5-nms-cropped.mp4 \
  -i h-max-10-nms-cropped.mp4 \
  -filter_complex hstack=inputs=3 \
  comparison.mp4
