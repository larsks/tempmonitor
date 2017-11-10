PORT = /dev/ttyUSB1
AMPY = ampy -p $(PORT)

CONFIG = config.json
SRCS = boot.py \
       main.py \
       hwconf.py \
       tempmonitor/__init__.py \
       tempmonitor/board.py \
       tempmonitor/discover.py \
       tempmonitor/monitor.py

all:

check:
	tox

install: .lastbuild

install-config:
	$(AMPY) put $(CONFIG) config.json
ifdef DEVICE
	[ -f "config_$(DEVICE).json" ] && \
		$(AMPY) put config_$(DEVICE).json config_local.json ||:
	[ -f "hwconf_$(DEVICE).py" ] && \
		$(AMPY) put hwconf_$(DEVICE).py hwconf_local.py ||:
endif

.lastbuild: $(SRCS)
	$(AMPY) mkdir --exists-okay tempmonitor
	for src in $?; do \
		$(AMPY) put $$src $$src; \
	done
	date > .lastbuild

clean:
	rm -f .lastbuild
