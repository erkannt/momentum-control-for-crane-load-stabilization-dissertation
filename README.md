# Dissertation Haarhoff

## Requirements

- pandoc
- pandoc-crossref
- pandoc-citeproc
- pandoc-include (the python version)
- xelatex
- python3

Install required python packages with `pip install -r tools/python-requirements.txt`.

## Generate PDF/HTML

First generate all plots and tikz/sketch illustrations.

````
make figures
````

````
make html
make pdf
````

Output and logs land in `output` folder.

## Automatic reload of PDF/HTML

Requires [entr](https://entrproject.org/)

````
find ./text ./figures ./style ./ -type f | entr make html
find ./text ./figures ./style ./ -type f | entr make pdf
````

To automatically reload the PDF use [Skim](https://skim-app.sourceforge.io/) on Mac.  
Under Linux entr recommends mupdf, since it can be told to reload from the commandline.

To automatically reload HTML you can use the `reload-brower` script from the entr project.

## Other useful commands

### Rerun plot or sketch commands

````
find ./ --name "*.py" | entr python /_
ls *.sk | entr -p ./sk2pdf /_
find *.sk | xargs -n1 ./sk2png
````

### Convert all mp4 to gif

Requires [gifify](https://github.com/vvo/gifify)

````
for f in $(find ./data -name "*.mp4"); do
gifify $f -o ${f/%.mp4/.gif}
done
````