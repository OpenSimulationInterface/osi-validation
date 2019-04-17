KPISDOCDIR=../docs/KPIs

.PHONY: clean

doxy: clean
	doxygen
	mkdir -p $(KPISDOCDIR)
	mv html $(KPISDOCDIR)

clean:
	rm -rf $(KPISDOCDIR)