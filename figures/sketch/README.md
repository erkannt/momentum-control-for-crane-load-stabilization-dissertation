# sketch illustrations

## Requires

- [sketch](http://www.frontiernet.net/~eugene.ressler/)
- [sketch-lib](https://alexdu.github.io/sketch-lib/)
- poppler-utils (for converting to png)

## Usage

- 'ls *.sk | entr -p ./sk2pdf /_'  
  watch for changed/new sketch files and render as pdf
- 'find *.sk | xargs -n1 ./sk2png'  
  render all sketch files as png
- PNGs rendered at 300dpi by default, change in 'sk2png'