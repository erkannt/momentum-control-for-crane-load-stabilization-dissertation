# Dissertation Haarhoff

[![Build Status](https://drone.rknt.de/api/badges/rknt/dissertation-haarhoff/status.svg)](https://drone.rknt.de/rknt/dissertation-haarhoff)

- build environment available as [container image](https://hub.docker.com/repository/docker/rknt/dissertation_builder)
- follow steps in `.drone.yml` or install [drone cli](https://docs.drone.io/cli/install/) and run `drone exec`

## Generate PDF/HTML

Output and logs land in `output` folder.

```
make html
make pdf
```

## Automatic reload of PDF/HTML

Requires [entr](https://entrproject.org/)

```
find ./text ./figures ./style ./ -type f | entr make html
find ./text ./figures ./style ./ -type f | entr make pdf
```

To automatically reload the PDF use [Skim](https://skim-app.sourceforge.io/) on Mac.
Under Linux entr recommends mupdf, since it can be told to reload from the commandline.

To automatically reload HTML you can use the `reload-browser` script from the entr project.

## latexrun fails to extract name from log

You need to adjust latex log settings to avoid line wraps.
See [this](https://tex.stackexchange.com/questions/52988/avoid-linebreaks-in-latex-console-log-output-or-increase-columns-in-terminal) tex.se post.

## Prepare PDF for Book Printing

Add extra pages to avoid the title page being glued to the cover.

````
pdftk A=diss-haarhoff.pdf B=blank.pdf cat B1 B1 A B1 B1 B1-end output diss-haarhoff.paddedWithBlanks.pdf
````

Add a 3mm margin to all pages, center the existing content but then shift it over to the outer edges by 10mm:

```
gs -q -dNOPAUSE -dBATCH \
   -o diss-haarhoff.increaseMediaSize.pdf \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS="/printer" \
   -dEmbedAllFonts=true \
   -sProcessColorModel=DeviceCMYK \
   -dFIXEDMEDIA \
   -dDEVICEWIDTHPOINTS=612 \
   -dDEVICEHEIGHTPOINTS=859 \
   -c "<< /CurrPageNum 1 def /Install { /CurrPageNum CurrPageNum 1 add def CurrPageNum 2 mod 1 eq {-28 9 translate} {37 9 translate} ifelse } bind  >> setpagedevice" \
   -f diss-haarhoff.paddedWithBlanks.pdf
```

Define the relevant page boxes so that we end up with a 3mm oversized media trimmed down to A4.

This requires [pdfboxer](https://github.com/nicknux/pdfboxer).

```
java -jar ~/tools/pdfboxer/bin/pdfboxer-0.0.1.jar \
     -trimBox 9,9,595,842 \
     -cropBox 9,9,595,842 \
     -bleedBox 0,0,612,859 \
     -sourceFile diss-haarhoff.increaseMediaSize.pdf \
     -destFile diss-haarhoff.withBleed.pdf
```
