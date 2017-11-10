PORT = /dev/ttyUSB1
AMPY = ampy -p $(PORT)

SRCS = boot.py \
       main.py \
       tempmonitor/__init__.py \
       tempmonitor/discover.py \
       tempmonitor/monitor.py \
       tempmonitor/sleep.py \
       tempmonitor/battery.py \
       config.json \
       tempmonitor/common.py

all:

check:
	tox

install: .lastbuild

.lastbuild: $(SRCS)
	$(AMPY) mkdir --exists-okay tempmonitor
	for src in $?; do \
		$(AMPY) put $$src $$src; \
	done
	date > .lastbuild

clean:
	rm -f .lastbuild
