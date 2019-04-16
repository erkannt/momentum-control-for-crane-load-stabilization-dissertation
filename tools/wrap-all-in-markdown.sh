#!/bin/sh
for f in *; do
  if  ! [ "$(sed -n '/^```/p;q' "$f")" ]; then
    echo "\`\`\`python"|cat - $f > /tmp/out && mv /tmp/out $f
    echo "\n\`\`\`" >> $f
  fi
done
