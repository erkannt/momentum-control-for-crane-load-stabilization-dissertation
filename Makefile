PY=python
PANDOC=pandoc

BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output
STYLEDIR=$(BASEDIR)/style

TEXTDIR=text
BIBFILE=$(BASEDIR)/$(TEXTDIR)/references.bib

# Build directory.
build = _build

plots_py := $(wildcard data/*/*plot.py)
plots_name := $(basename $(notdir $(plots_py)))
plots_pdf := $(plots_name:%=$(build)/figures/%.pdf)
plots_svg := $(plots_name:%=$(build)/figures/%.svg)

VPATH := $(wildcard data/*)

test:
	@echo "plots:			$(plots_svg)"
	@echo "vpath:			$(VPATH)"

$(build):
	mkdir -p $(build)

$(build)/figures: 
	mkdir -p $(build)/figures

$(build)/figures/%.svg: %.py | $(build)/figures
	python $< $(build)/figures
	sed -i "" 's/width.*pt\"//g' $@
	sed -i "" 's/height.*pt\"//g' $@

$(build)/figures/%.pdf: %.py | $(build)/figures
	python $<

html: $(plots_svg) | $(build)
	@echo "fake build html"

clean:
	rm -r $(build)