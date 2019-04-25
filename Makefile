PY=python
PANDOC=pandoc
LATEXRUN := $(abspath tools/latexrun)

STYLEDIR := $(abspath style)
BIBFILE := $(abspath text/references.bib)

# Build directory.
build = _build

text := $(wildcard text/*.md)

plots_py := $(wildcard data/*/*.py)
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

gifs := $(wildcard figures/*.gif)
gif_names := $(basename $(notdir $(gifs)))
gifaspng := $(gif_names:%=$(build)/figures/%.png)

VPATH := $(wildcard data/*):figures:text

test:
	@echo "vpath:			$(VPATH)"
	@echo "plots:			$(plots_name)"
	@echo "sketches:	$(sketches_name)"
	@echo "tikz:			$(tikz_name)"
	@echo "text:			$(text)"
	@echo "gifs:			$(gifs)"
	@echo "gifs:			$(gif_names)"
	@echo "gifs:			$(gifaspng)"

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
	@echo "$< >>> $@"
	cd $(dir $(abspath $<)) && \
	$(LATEXRUN) -O $(build)/latexrun/$(basename $@).latexrun \
	  -o $(abspath $@) --latex-cmd pdflatex --bibtex-cmd biber $(notdir $<)

$(build)/figures/%.pdf: %.tex | $(build)/figures
	@echo "$< >>> $@"
	cd $(dir $(abspath $<)) && \
	$(LATEXRUN) -O $(build)/latexrun/$(basename $@).latexrun \
	  -o $(abspath $@) --latex-cmd pdflatex --bibtex-cmd biber $(notdir $<)
	pdfcrop $@ $@ -margins "5 5 5 5"

$(build)/figures/%.png: %.pdf | $(build)/figures
	pdfcrop $< $< -margins "5 5 5 5"
	convert -flatten -density 300 -define profile:skip=ICC $< -quality 90 $@

$(build)/figures/%.png: %.gif | $(build)/figures
	convert '$<[0]' $@

html-figures: $(plots_svg) $(sketches_png) $(tikz_png) staticfigs | $(build)/figures

html: html-figures | $(build)
	pandoc text/*.md \
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

pdf-figures: $(plots_pdf) $(sketches_pdf) $(tikz_pdf) $(gifaspng) staticfigs | $(build)/figures

pdf: pdf-figures $(build)/diss-haarhoff.pdf | $(build)

$(build)/diss-haarhoff.tex: $(text) style/preamble.tex style/template.tex
	rsync -a --delete text $(build)/
	sed -i "" 's/\.svg/\.pdf/g' $(build)/text/*.md
	sed -i "" 's/\.gif/\.png/g' $(build)/text/*.md
	pandoc $(build)/text/*.md \
	-F pandoc-crossref \
	-F pandoc-include \
	-o "$(build)/diss-haarhoff.tex" \
	-H "$(STYLEDIR)/preamble.tex" \
	--template="$(STYLEDIR)/template.tex" \
	--bibliography="$(BIBFILE)" \
	-V fontsize=12pt \
	-V papersize=a4paper \
	-V documentclass=report \
	-N \
	--csl="$(STYLEDIR)/ref_format.csl" \

clean:
	rm -r $(build)