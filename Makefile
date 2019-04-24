PY=python
PANDOC=pandoc

BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output
STYLEDIR=$(BASEDIR)/style

TEXTDIR=text
BIBFILE=$(BASEDIR)/$(TEXTDIR)/references.bib

# Build directory.
build = _build

text := $(wildcard text/*.md)

plots_py := $(wildcard data/*/*plot.py)
plots_name := $(basename $(notdir $(plots_py)))
plots_pdf := $(plots_name:%=$(build)/figures/%.pdf)
plots_svg := $(plots_name:%=$(build)/figures/%.svg)

sketches := $(wildcard figures/*.sk)
sketches_name := $(basename $(notdir $(sketches)))
sketches_pdf := $(sketches_name:%=$(build)/figures/%.pdf)
sketches_png := $(sketches_name:%=$(build)/figures/%.png)

tikz := $(wildcard figures/*.tex)
tikz_name := $(basename $(notdir $(tikz)))
tikz_pdf := $(tikz_name:%=$(build)/figures/%.pdf)
tikz_png := $(tikz_name:%=$(build)/figures/%.png)

VPATH := $(wildcard data/*):figures:text

test:
	@echo "vpath:			$(VPATH)"
	@echo "plots:			$(plots_name)"
	@echo "sketches:	$(sketches_name)"
	@echo "tikz:			$(tikz_name)"
	@echo "text:			$(text)"

$(build):
	mkdir -p $(build)
	mkdir -p $(build)/logs

$(build)/figures: 
	mkdir -p $(build)/figures

$(build)/figures/%.svg: %.py | $(build)/figures
	python $< $@
	sed -i "" 's/width.*pt\"//g' $@
	sed -i "" 's/height.*pt\"//g' $@

$(build)/figures/%.pdf: %.py | $(build)/figures
	python $< $@

staticfigs:
	rsync -a --exclude="*.sk" --exclude="*.tex" figures/ $(build)/figures

%.tex: %.sk
	@echo $@ $<
	sketch -Te $< -o $@

%.pdf: %.tex
	tools/latexrun -O $(build)/latexrun/$(basename $@).latexrun \
		--latex-cmd pdflatex --bibtex-cmd biber $<

$(build)/figures/%.png: %.pdf | $(build)/figures
	pdfcrop $< $< -margins "5 5 5 5"
	convert -flatten -density 300 -define profile:skip=ICC $< -quality 90 $@

html-figures: $(plots_svg) $(sketches_png) $(tikz_png) staticfigs | $(build)/figures

html: html-figures | $(build)
	pandoc "$(TEXTDIR)"/*.md \
		-o "$(build)/thesis.html" \
		--mathml \
		--standalone \
		-F pandoc-crossref \
		-F pandoc-include \
		--template="$(STYLEDIR)/template.html" \
		--bibliography="$(BIBFILE)" \
		--csl="$(STYLEDIR)/ref_format.csl" \
		--include-in-header="$(STYLEDIR)/style.css" \
		--toc \
		--number-sections \
		--verbose 

%.html: %.md html-figures
	pandoc $< \
		-o "$(build)/$@" \
		-M title="$(basename $@)" \
		--mathml \
		--standalone \
		-F pandoc-crossref \
		-F pandoc-include \
		--template="$(STYLEDIR)/template.html" \
		--bibliography="$(BIBFILE)" \
		--csl="$(STYLEDIR)/ref_format.csl" \
		--include-in-header="$(STYLEDIR)/style.css" \
		--toc \
		--number-sections \
		--verbose 

clean:
	rm -r $(build)