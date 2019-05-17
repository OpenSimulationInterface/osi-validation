# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
DOCDIR        = ${CURDIR}/html

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

gh-pages:
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)
	rm -rf $(DOCDIR)
	mkdir $(DOCDIR)
	cp -r $(BUILDDIR)/html/* $(DOCDIR)
	@echo "The HTML pages are in $(DOCDIR)"
	@echo "Compilation of the KPIs documentation"
	@$(MAKE) KPIDOCDIR="$(DOCDIR)/KPIs" doxy -C ../KPIs >> /dev/null > /dev/null 2>&1
	@echo done.

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
