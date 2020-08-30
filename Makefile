# OS specific sed
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
SED=sed -i
endif
ifeq ($(UNAME), Darwin)
SED=sed -i ""
endif

# Required executables
PYTHON=python3
PANDOC=pandoc
LATEXRUN := $(abspath tools/latexrun)
LATEX=pdflatex
BIB=biber
SINGLEPAGE=singlepage
PDF2SVG=pdf2svg

# Project Settings
build = _build
name = diss-haarhoff
version := $(shell ./tools/pretty_git_sha.sh)
bibfile := $(abspath text/bibliography.yaml)
stylefolder := $(abspath style)
pandoc-html-flags = --verbose \
	-F pandoc-crossref \
	-F pandoc-include-code \
	-F pandoc-include \
	--bibliography="$(bibfile)" \
	--include-in-header="$(stylefolder)/style.css" \
	--include-after-body=$(stylefolder)/anchors.js \
	--template="$(stylefolder)/template.html" \
	--mathml \
	--standalone \
	--csl="$(stylefolder)/ref_format.csl" \
	--toc \
	--metadata date="`date "+%B %e, %Y"`" \
	--metadata version="$(version)" \
	--number-sections
pandoc-tex-flags = --verbose \
	-F pandoc-crossref \
	-F pandoc-include-code \
	-F pandoc-include \
	--lua-filter=tools/short-captions.lua \
	-H "$(stylefolder)/preamble.tex" \
	--template="$(stylefolder)/template.tex" \
	--bibliography="$(bibfile)" \
	--number-sections \
	--metadata date="`date "+%B %e, %Y"`" \
	--metadata version="$(version)" \
	--csl="$(stylefolder)/ref_format.csl"
pandoc-epub-flags = --verbose \
	-F pandoc-crossref \
	-F pandoc-include-code \
	-F pandoc-include \
	--template="$(stylefolder)/template.epub.html" \
	--bibliography="$(bibfile)" \
	--number-sections \
	--metadata date="`date "+%B %e, %Y"`" \
	--metadata version="$(version)" \
	--mathjax \
	--epub-cover-image cover.jpeg \
	--csl="$(stylefolder)/ref_format.csl"
ghostscript-flags = -sDEVICE=pdfwrite \
  -dCompatibilityLevel=1.4 \
  -dPDFSETTINGS=/printer \
  -dPrinted=false \
	-dNOPAUSE \
	-dQUIET \
	-dBATCH
# Where make looks for source files
VPATH := $(wildcard data/*):figures:text

# Source collections
text := $(wildcard text/*.md)
images := $(wildcard figures/*.png) $(wildcard figures/*.jpg) $(wildcard figures/*.svg)
mov := $(wildcard figures/*.mp4)
plots_py := $(wildcard data/*/*.py)
sketches := $(wildcard figures/*.sk)
tikz := $(wildcard figures/*.tex)

html-style := $(wildcard $(stylefolder)/*.html) $(wildcard $(stylefolder)/*.js) $(wildcard $(stylefolder)/*.css)
tex-style := $(wildcard $(stylefolder)/*.tex)
ref-style = $(stylefolder)/ref_format.csl

# Target collections
text4tex := $(addprefix $(build)/text4tex/, $(notdir $(text)))
text4epub := $(addprefix $(build)/text4epub/, $(notdir $(text)))
static := $(images:%=$(build)/%) $(mov:%=$(build)/%)
svgaspdf := $(static:.svg=.pdf)

plots_name := $(basename $(notdir $(plots_py)))
plots_pdf := $(plots_name:%=$(build)/figures/%.pdf)
plots_svg := $(plots_name:%=$(build)/figures/%.svg)

sketches_name := $(basename $(notdir $(sketches)))
sketches_pdf := $(sketches_name:%=$(build)/figures/%.pdf)
sketches_png := $(sketches_name:%=$(build)/figures/%.png)

tikz_name := $(basename $(notdir $(tikz)))
tikz_pdf := $(tikz_name:%=$(build)/figures/%.pdf)
tikz_png := $(tikz_name:%=$(build)/figures/%.png)

mov_names := $(basename $(notdir $(mov)))
gif := $(mov_names:%=$(build)/figures/%.gif)
gifaspng := $(mov_names:%=$(build)/figures/%.png)

# High-Level Targets
main: html pdf standalone

all: html pdf standalone epub bigzip

html: html-figures $(build)/$(name).html | $(build)

pdf: pdf-figures $(build)/$(name).pdf | $(build)

ebook: epub

epub: pdf-figures html-figures code4epub $(build)/$(name).epub | $(build)

standalone: $(build)/$(name).standalone.html | html

zip: $(build)/$(name).zip

bigzip: $(build)/$(name).zip

html-figures: $(plots_pdf) $(plots_svg) $(sketches_png) $(tikz_png) $(gif) $(static) | $(build)/figures

pdf-figures: $(plots_pdf) $(sketches_png) $(tikz_png) $(gifaspng) $(static) $(svgaspdf) | $(build)/figures

# HTML Targets
$(build)/$(name).html: $(text) $(html-style) $(ref-style) | $(build)
	$(PANDOC) text/*.md -o $@ $(pandoc-html-flags)

%.html: %.md  $(html-style) $(ref-style) html-figures | $(build)
	$(PANDOC) $< -o "$@" -M title="$(basename $@)" $(pandoc-html-flags)

$(build)/$(name).standalone.html: $(build)/$(name).html
	cd $(build) && \
	$(SINGLEPAGE) $(name).html > $(name).standalone.html
	$(SED) 's/<math disp/ <math disp/g' $@

# TeX Target
$(build)/$(name).tex: pdf-figures $(text4tex) $(tex-style) $(ref-style)
	$(PANDOC) $(build)/text4tex/*.md -o "$(build)/$(name).tex" $(pandoc-tex-flags)

$(build)/text4tex/%.md: %.md | $(build)/text
	cp $< $@
	$(SED) 's/\.svg/\.pdf/g' $@
	$(SED) 's/\.gif/\.png/g' $@
	$(SED) 's/^```{.*/CODE LISTING REMOVED FROM PDF -- /g' $@
	$(SED) 's/^```/AVAILABLE IN HTML FILE/g' $@

# ZIP of all
$(build)/$(name).zip: html pdf standalone epub
	cd $(build) && \
	cp $(name).pdf $(name).orig.pdf && \
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$(name).pdf $(name).orig.pdf && \
	zip -r $(name).zip $(name).pdf $(name).standalone.html $(name).epub $(name).html figures

# eBook Targets
$(build)/$(name).epub: $(text4epub) $(ref-style) | $(build)
	cp cover.jpeg $(build)/cover.jpeg && \
	cd $(build) && \
	$(PANDOC) text4epub/*.md -o $(notdir $@) $(pandoc-epub-flags)

$(build)/text4epub/%.md: %.md | $(build)/text
	cp $< $@
	$(SED) 's/\.gif/\.png/g' $@

# Required folders
$(build):
	mkdir -p $(build)

$(build)/figures:
	mkdir -p $(build)/figures

$(build)/text:
	mkdir -p $(build)/text
	mkdir -p $(build)/text4tex
	mkdir -p $(build)/text4epub

# Convert pdf plots to svg as matplotlib borks tex symbols in svg
$(build)/figures/%.svg: $(build)/figures/%.pdf | $(build)/figures
	$(PDF2SVG) $< $@
	$(SED) 's/width.*pt\"//g' $@
	$(SED) 's/height.*pt\"//g' $@

# Plots from python scripts
$(build)/figures/%.pdf: %.py | $(build)/figures
	$(PYTHON) $< $@

# Static files that need to be copied
$(build)/figures/%.png: %.png | $(build)/figures
	cp $< $@

$(build)/figures/%.jpg: %.jpg | $(build)/figures
	cp $< $@

$(build)/figures/%.mp4: %.mp4 | $(build)/figures
	cp $< $@

$(build)/figures/%.svg: %.svg | $(build)/figures
	cp $< $@

$(build)/figures/%.pdf: %.svg | $(build)/figures
	rsvg-convert --zoom=3.0 -f pdf -o $@ $<

code4epub:
	cp -r code $(build)/code

# sketch >>> TeX
%.tex: %.sk
	@echo $@ $<
	sketch -Te $< -o $@

# TeX >>> PDF
%.pdf: %.tex
	@echo "$< >>> $@"
	cd $(dir $(abspath $<)) && \
	$(LATEXRUN) -O $(abspath $(build))/latexrun/$(basename $@).latexrun \
	  -o $(abspath $@) --latex-cmd $(LATEX) --bibtex-cmd $(BIB) $(notdir $<)

# TeX >>> PDF with crop for figures
$(build)/figures/%.pdf: %.tex | $(build)/figures
	@echo "$< >>> $@"
	cd $(dir $(abspath $<)) && \
	$(LATEXRUN) -O $(abspath $(build))/latexrun/$(basename $@).latexrun \
	  -o $(abspath $@) --latex-cmd $(LATEX) --bibtex-cmd $(BIB) $(notdir $<)
	pdfcrop $@ $@ -margins "5 5 5 5"

# Other files conversions
$(build)/figures/%.png: %.pdf | $(build)/figures
	pdfcrop $< $< -margins "5 5 5 5"
	convert -flatten -density 300 -define profile:skip=ICC $< -quality 90 $@

$(build)/figures/%.png: %.mp4 | $(build)/figures
	ffmpeg -y -sseof -1 -i $< -vframes 1 -q:v 2 -vf scale=1024:-2 $@
	convert $@ -gravity south -undercolor black -fill yellow -font Lato-Regular -pointsize 18 -annotate +0+0 "This should be a video. Please see HTML-version of this document." $@

$(build)/figures/%.gif: %.mp4 | $(build)/figures
	gifify $< --resize '800:-1' -o $@

$(build)/figures/robot_comp.gif: robot_comp.mp4 | $(build)/figures
	gifify $< --resize '800:-1' --fps 30 --colors 160 -o $@

clean-all:
	rm -r $(build)

clean-pdf:
	rm -r $(build)/text
	rm  $(build)/*.tex
	rm  $(build)/*.pdf

clean:
	rm -r $(build)/text*
	rm $(build)/diss-haarhoff*
