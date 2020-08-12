# Dissertation Haarhoff

[![Build Status](https://drone.rknt.de/api/badges/rknt/dissertation-haarhoff/status.svg)](https://drone.rknt.de/rknt/dissertation-haarhoff)

- build environment available as [container image](https://hub.docker.com/repository/docker/rknt/dissertation_builder)
- follow steps in `.drone.yml` or install [drone cli](https://docs.drone.io/cli/install/) and run `drone exec`

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

## latexrun fails to extract name from log

You need to adjust latex log settings to avoid line wraps.
See [this](https://tex.stackexchange.com/questions/52988/avoid-linebreaks-in-latex-console-log-output-or-increase-columns-in-terminal) tex.se post.