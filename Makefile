TARGET = /dev/ttyUSB0
AMPY = ampy -p $(TARGET)

CONFIG = config.json
TEMPMONITOR_FILES = \
	boot.py	\
	main.py	\
	main_stage2.py	\
	hwconf.py	\
	board.py	\
	otaserver.py	\
	tempmonitor/__init__.py	\
	tempmonitor/board.py	\
	tempmonitor/monitor.py	\

NOGGIN_FILES = \
	noggin/__init__.py \
	noggin/app.py \
	noggin/http.py

all:

check:
	tox

install: install-tempmonitor install-noggin

install-config:
	$(AMPY) put $(CONFIG) config.json
ifdef DEVICE
	[ -f "config_$(DEVICE).json" ] && \
		$(AMPY) put config_$(DEVICE).json config_local.json ||:
	[ -f "hwconf_$(DEVICE).py" ] && \
		$(AMPY) put hwconf_$(DEVICE).py hwconf_local.py ||:
endif

install-tempmonitor: .lastinstall-tempmonitor
install-noggin: .lastinstall-noggin

.lastinstall-tempmonitor: $(TEMPMONITOR_FILES)
	$(AMPY) mkdir --exists-okay tempmonitor
	for src in $?; do \
		$(AMPY) put $$src $$src; \
	done
	date > $@

.lastinstall-noggin: $(addprefix noggin/,$(NOGGIN_FILES))
	$(AMPY) mkdir --exists-okay noggin
	for src in $(NOGGIN_FILES); do \
		$(AMPY) put noggin/$$src $$src; \
	done
	date > $@

clean:
	rm -f .lastinstall-noggin .lastinstall-tempmonitor

refresh: clean
	$(AMPY) rmdir tempmonitor
