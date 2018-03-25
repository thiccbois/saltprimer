# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = ../venv/bin/sphinx-build
SPHINXPROJ    = Primer
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "${BUILDDIR}" $(SPHINXOPTS) $(O)
apidoc:
	rm -rf source/apidoc
	../venv/bin/sphinx-apidoc -f -A "Stefan Schweer" -H "Primer" -F -d 4 -e -P -o "source/apidoc" "../primer"
	rm -rf source/apidoc/index.rst



gh-pages: apidoc html
	rm -rf ../docs/*
	cp -rf build/html/* ../docs/

.PHONY: help apidoc gh-pages Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


