BUILDDIR=build
FILE=A_8_1
PREFIX=tollander_

pdf:
	mkdir $(BUILDDIR) -p
	pandoc $(FILE).md \
	--from=markdown+raw_tex+tex_math_single_backslash \
	--to=latex \
	--output=$(BUILDDIR)/$(PREFIX)$(FILE).pdf \
	--pdf-engine=xelatex \
	--variable urlcolor=cyan \
	--variable papersize=a4paper \
	--variable links-as-notes \
	--filter pandoc-citeproc \
	--bibliography=bibliography.bib \
	--csl=https://raw.githubusercontent.com/citation-style-language/styles/master/harvard-anglia-ruskin-university.csl \


notebook-pdf:
	jupyter nbconvert A_5_2.ipynb --to pdf


clean:
	rm $(BUILDDIR)/*
