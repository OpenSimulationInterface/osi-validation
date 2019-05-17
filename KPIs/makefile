KPISDOCDIR=${KPIDOCDIR}

.PHONY: clean

doxy: clean
	doxygen >> /dev/null > /dev/null 2>&1
	mv html $${KPIDOCDIR:-here}

clean:
	rm -rf $${KPIDOCDIR:-here}/*
