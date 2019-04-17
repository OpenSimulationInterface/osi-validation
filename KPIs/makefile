KPISDOCDIR=../docs/KPIs

.PHONY: clean

doxy: clean
	doxygen
	mv html $(KPISDOCDIR)

clean:
	rm -rf $(KPISDOCDIR)