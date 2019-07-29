#!/bin/sh

for f in *kg.mp4; do
  ffmpeg -y -i $f -vf crop=1060:1200:in_w/2-out_w/2+40:in_h/2-out_h/2-100 ${f/%.mp4/-cropped.mp4}
done
ffmpeg -y \
  -i lab-setup-5m-10kg-cropped.mp4 \
  -i l1-24-19m-2400kg-cropped.mp4 \
  -i 380ec-b16-83m-15660kg-cropped.mp4 \
  -filter_complex hstack=inputs=3 \
  comparison.mp4
