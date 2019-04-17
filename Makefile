PY=python
PANDOC=pandoc

BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output
STYLEDIR=$(BASEDIR)/style

TEXTDIR=text
FIGDIR=figures
BIBFILE=$(BASEDIR)/$(TEXTDIR)/references.bib

help:
	@echo ' 																	  '
	@echo 'Makefile for the Markdown thesis                                       '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make html                        generate a web version             '
	@echo '   make pdf                         generate a PDF file  			  '
	@echo ' 																	  '
	@echo 'get local templates with: pandoc -D latex/html/etc	  				  '
	@echo 'or generic ones from: https://github.com/jgm/pandoc-templates		  '

all: plots figures html pdf

pdf:
	rsync -a --delete $(BASEDIR)/$(TEXTDIR) $(OUTPUTDIR)/
	sed -i "" 's/\.svg/\.png/g' $(OUTPUTDIR)/$(TEXTDIR)/*.md
	cd $(OUTPUTDIR)
	pandoc $(TEXTDIR)/*.md \
		-o "$(OUTPUTDIR)/thesis.pdf" \
		-H "$(STYLEDIR)/preamble.tex" \
		-F pandoc-crossref \
		--template="$(STYLEDIR)/template.tex" \
		--bibliography="$(BIBFILE)" &>$(OUTPUTDIR)/pandoc-pdf.log \
		--csl="$(STYLEDIR)/ref_format.csl" \
		--highlight-style pygments \
		-V fontsize=12pt \
		-V papersize=a4paper \
		-V documentclass=article \
		-N \
		--pdf-engine=xelatex \
		--verbose &>$(OUTPUTDIR)/latex-pdf.log
	cat $(OUTPUTDIR)/*-pdf.log | grep -i warning

html:
	pandoc "$(TEXTDIR)"/*.md \
		-o "$(OUTPUTDIR)/thesis.html" \
		--mathml \
		--standalone \
		-F pandoc-crossref \
		-F pandoc-include \
		--template="$(STYLEDIR)/template.html" \
		--bibliography="$(BIBFILE)"  &>$(OUTPUTDIR)/pandoc-html.log \
		--csl="$(STYLEDIR)/ref_format.csl" \
		--include-in-header="$(STYLEDIR)/style.css" \
		--toc \
		--number-sections \
		--verbose
	cat $(OUTPUTDIR)/*-html.log | grep -i warning || true

plots:
	./tools/plots.sh

figures:
	rsync -a --delete $(BASEDIR)/$(FIGDIR) $(OUTPUTDIR)/
	find $(OUTPUTDIR)/$(FIGDIR) -name "*.sk" | xargs -n1 ./tools/sk2png
	find $(OUTPUTDIR)/$(FIGDIR) -name "*.tex" | xargs -n1./tools/tex2png

clean:
	rm -r ./output/*

.PHONY: help all pdf html plots figures clean
