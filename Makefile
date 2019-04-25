# Required executables
PY=python
PANDOC=pandoc
LATEXRUN := $(abspath tools/latexrun)
LATEX=pdflatex
BIB=biber
SINGLEPAGE=singlepage

# Project Settings
build = _build
name = diss-haarhoff
bibfile := $(abspath text/references.bib)
stylefolder := $(abspath style)
pandoc-html-flags = --verbose \
	-F pandoc-crossref \
	-F pandoc-include \
	--bibliography="$(bibfile)" \
	--include-in-header="$(stylefolder)/style.css" \
	--template="$(stylefolder)/template.html" \
	--mathml \
	--standalone \
	--csl="$(stylefolder)/ref_format.csl" \
	--toc \
	--number-sections
pandoc-tex-flags = --verbose \
	-F pandoc-crossref \
	-F pandoc-include \
	-H "$(stylefolder)/preamble.tex" \
	--template="$(stylefolder)/template.tex" \
	--bibliography="$(bibfile)" \
	-V fontsize=12pt \
	-V papersize=a4paper \
	-V documentclass=report \
	-N \
	--csl="$(stylefolder)/ref_format.csl"

# Where make looks for source files
VPATH := $(wildcard data/*):figures:text

# Source collections
text := $(wildcard text/*.md)
images := $(wildcard figures/*.png) $(wildcard figures/*.jpg)
mov := $(wildcard figures/*.mp4)
plots_py := $(wildcard data/*/*.py)
sketches := $(wildcard figures/*.sk)
tikz := $(wildcard figures/*.tex)

html-style := $(wildcard $(stylefolder)/*.html) $(wildcard $(stylefolder)/*.css)
tex-style := $(wildcard $(stylefolder)/*.tex)
ref-style = $(stylefolder)/ref_format.csl

# Target collections
static := $(images:%=$(build)/%) $(mov:%=$(build)/%)

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
all: html pdf standalone

html: html-figures $(build)/$(name).html | $(build)

pdf: pdf-figures $(build)/$(name).pdf | $(build)

standalone: $(build)/$(name).standalone.html

html-figures: $(plots_svg) $(sketches_png) $(tikz_png) $(gif) $(static) | $(build)/figures

pdf-figures: $(plots_pdf) $(sketches_pdf) $(tikz_pdf) $(gifaspng) $(static) | $(build)/figures

# HTML Targets
$(build)/$(name).html: $(text) $(html-style) $(ref-style) | $(build)
	pandoc text/*.md -o $@ $(pandoc-html-flags)

%.html: %.md  $(html-style) $(ref-style) html-figures | $(build)
	pandoc $< -o "$@" -M title="$(basename $@)" $(pandoc-html-flags)

$(build)/$(name).standalone.html: $(build)/$(name).html
	cd $(build) && \
	$(SINGLEPAGE) $(name).html > $(name).standalone.html

# TeX Target
$(build)/$(name).tex: $(text) $(tex-style) $(ref-style)
	rsync -av --delete text/ $(build)/text
	sed -i "" 's/\.svg/\.pdf/g' $(build)/text/*.md
	sed -i "" 's/\.gif/\.png/g' $(build)/text/*.md
	pandoc $(build)/text/*.md -o "$(build)/$(name).tex" $(pandoc-tex-flags)

# Required folders
$(build):
	mkdir -p $(build)
	mkdir -p $(build)/logs

$(build)/figures: 
	mkdir -p $(build)/figures

# Plots from python scripts
$(build)/figures/%.svg: %.py | $(build)/figures
	python $< $@
	sed -i "" 's/width.*pt\"//g' $@
	sed -i "" 's/height.*pt\"//g' $@

$(build)/figures/%.pdf: %.py | $(build)/figures
	python $< $@

# Static files that need to be copied
$(build)/figures/%.png: %.png | $(build)/figures
	cp $< $@

$(build)/figures/%.jpg: %.jpg | $(build)/figures
	cp $< $@

$(build)/figures/%.mp4: %.mp4 | $(build)/figures
	cp $< $@

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
	ffmpeg -ss 00:00:00 -i $< -vframes 1 -q:v 2 $@

$(build)/figures/%.gif: %.mp4 | $(build)/figures
	gifify $< --resize '800:-1' -o $@

clean:
	rm -r $(build)

test:
	@echo "images:		$(static)"