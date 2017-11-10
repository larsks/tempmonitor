PORT = /dev/ttyUSB1
AMPY = ampy -p $(PORT)

CONFIG = config.json
SRCS = boot.py \
       main.py \
       tempmonitor/__init__.py \
       tempmonitor/board.py \
       tempmonitor/discover.py \
       tempmonitor/monitor.py \
       tempmonitor/battery.py \
       tempmonitor/common.py

all:

check:
	tox

install: .lastbuild

install-config:
	$(AMPY) put $(CONFIG) config.json

.lastbuild: $(SRCS)
	$(AMPY) mkdir --exists-okay tempmonitor
	for src in $?; do \
		$(AMPY) put $$src $$src; \
	done
	date > .lastbuild

clean:
	rm -f .lastbuild
