# Dissertation Haarhoff

This repo contains all text, data, code and figure inputs for my dissertation.
It also includes tooling to generate HTML, PDF and ePub versions from these inputs.

- [HTML version that includes video and code listings](https://public.rknt.de/diss-haarhoff/diss-haarhoff.html)
- [PDF version of record published by RWTH Aachen University](https://doi.org/10.18154/RWTH-2021-08190)

Other formats available:

- [ePub](https://public.rknt.de/diss-haarhoff/diss-haarhoff.epub)
- [PDF with hyperlinks](https://public.rknt.de/diss-haarhoff/diss-haarhoff.orig.pdf)
- [singlefile HTML version](https://public.rknt.de/diss-haarhoff/diss-haarhoff.standalone.html) (all media, stylesheets etc. inlined in the HTML as base64 string; 150MB)

To cite the thesis use: [10.18154/RWTH-2021-08190](https://doi.org/10.18154/RWTH-2021-08190)

To cite this repo use: [10.5281/zenodo.5841504](https://doi.org/10.5281/zenodo.5841504)

## Abstract

> The digitalization of the construction industries planning and execution phases, coupled with advances in automation technology has led to a renaissance for construction robotics. Current efforts to provide robots for the execution of digital construction plans revolve around either the adaptation of industrial robots for the construction site, highly specialized custom robots or the digitalization of existing construction equipment. However, there is currently no robotics approach that addresses the very large work envelope that constitutes a construction site.
>
> This work therefore evaluates the feasibility of operating robots and other kinematic systems hanging from a regular crane. A crane’s hook is not a stable base for a robot. Movements of the robot as well as external forces would lead to motions and oscillations. The robot would therefore not be able to execute accurate movements.
>
> Stabilizing a platform at the hook to create a useable base for robots requires adding further means of control to said platform. Three approaches are known: additional ropes, propulsive devices and momentum control devices. This work studies the use of a specific type of momentum control device, so called control moment gyroscopes. These are an established technology for the stabilization of ships and also the reorientation of spacecraft. By gimbaling a fast spinning rotor orthogonal to its axis of rotation, CMGs are able to generate torque through the principle of gyroscopic reaction. They are thereby able to generate torque in mid-air and unlike additional ropes or propulsive devices do not interfere with their environment.
>
> The following work develops equations of motion and a model for the crane-CMG-robot system. A general control strategy is laid out and a simple PD-based controller is designed. The model is validated through a variety of simulations and used to understand the critical interactions between the three systems. The ability of a CMG platform to predictively compensate the torques produced by a robot and thereby improve its path accuracy is shown through simulation. It is also shown how such a platform can help dampen hook and load oscillations. The simulations not only show the potential of the approach, but also allow the work to develop sizing guidelines and identify critical areas for future research. The work therefore closes by laying out the critical path to bringing this approach to the construction site.
## Generating HTML, PDF and ePub versions

The various versions are generated from markdown using the `Makefile` that relies on a bunch of tools like `pandoc`, `ffmpeg` etc.

- build environment available as [container image](https://hub.docker.com/repository/docker/rknt/dissertation_builder)
- follow steps in `.drone.yml` or install [drone cli](https://docs.drone.io/cli/install/) and run `drone exec`

The conversion steps are:

- md > HTML
- md > ePub
- md > LaTex > PDF

Figures are generated for the various formats as needed. Figures can be provided as SVG, PDF, PNG, JPEG, MP4, tikz or sk files.
For PDF and ePub outputs all videos get replaced with single frames using `ffmpeg` and some `sed` magic.

## Misc. notes on building the content
### Automatic reload of PDF/HTML

Requires [entr](https://entrproject.org/)

```
find ./text ./figures ./style ./ -type f | entr make html
find ./text ./figures ./style ./ -type f | entr make pdf
```

To automatically reload the PDF use [Skim](https://skim-app.sourceforge.io/) on Mac.
Under Linux entr recommends mupdf, since it can be told to reload from the commandline.

To automatically reload HTML you can use the `reload-browser` script from the entr project.

### latexrun fails to extract name from log

You need to adjust latex log settings to avoid line wraps.
See [this](https://tex.stackexchange.com/questions/52988/avoid-linebreaks-in-latex-console-log-output-or-increase-columns-in-terminal) tex.se post.

### Prepare PDF for Book Printing

Add extra pages to avoid the title page being glued to the cover.

````
pdftk A=diss-haarhoff.pdf B=blank.pdf cat B1 B1 A B1 B1 B1-end output diss-haarhoff.paddedWithBlanks.pdf
````

Add a 3mm margin to all pages, center the existing content but then shift it over to the outer edges:

```
gs -q -dNOPAUSE -dBATCH \
   -o diss-haarhoff.increaseMediaSize.pdf \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS="/printer" \
   -dEmbedAllFonts=true \
   -sProcessColorModel=DeviceGray \
   -sColorConversionStrategy=Gray \
   -dOverrideICC \
   -dFIXEDMEDIA \
   -dDEVICEWIDTHPOINTS=436.535 \
   -dDEVICEHEIGHTPOINTS=612.283 \
   -c "<< /CurrPageNum 1 def /Install { /CurrPageNum CurrPageNum 1 add def CurrPageNum 2 mod 1 eq {0.7 0.7 scale -18 9 translate} {0.7 0.7 scale 27 9 translate} ifelse } bind  >> setpagedevice" \
   -f diss-haarhoff.paddedWithBlanks.pdf
```

Define the relevant page boxes so that we end up with a 3mm oversized media trimmed down to A4.

This requires [pdfboxer](https://github.com/nicknux/pdfboxer).

```
java -jar ~/tools/pdfboxer/bin/pdfboxer-0.0.1.jar \
     -trimBox 9,9,419.528,595.276 \
     -cropBox 9,9,419.528,595.276 \
     -bleedBox 0,0,436.535,612.283 \
     -sourceFile diss-haarhoff.increaseMediaSize.pdf \
     -destFile diss-haarhoff.withBleed.pdf
```
