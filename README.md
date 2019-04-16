# Dissertation Haarhoff

## Generate PDF/HTML

Output and logs land in `output` folder.

````
make html
make pdf
````

## Automatic reload of PDF/HTML

Requires [entr](https://entrproject.org/)

````
find ./text ./figures ./style ./ -type f | entr make html
find ./text ./figures ./style ./ -type f | entr make pdf
````

To automatically reload the PDF use [Skim](https://skim-app.sourceforge.io/) on Mac.  
Under Linux entr recommends mupdf, since it can be told to reload from the commandline.

To automatically reload HTML you can use the `reload-browser` script from the entr project.