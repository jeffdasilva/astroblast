###############################################################################
#
# Jeff DaSilva
# Copyright 2016 All Rights Reserved
#
###############################################################################

ifeq ($(DEBUG),1)
$(info python.mk included)
endif


#############################
PYTHON.PACKAGES = $(foreach subdir,* */* */*/* */*/*/*,$(patsubst %/__init__.py,%,$(wildcard $(subdir)/__init__.py)))
PYTHON.SRC := $(wildcard *.py) $(foreach pkg,$(PYTHON_PACKAGES),$(wildcard $(pkg)/*.py))
PYTHON.MAIN := $(wildcard *.py)
#############################


#############################

PYTHON.UNITTEST_STAMPS := $(strip \
	$(patsubst %.py,stamps/%.unittest,\
	$(filter-out %__init__.py,\
	$(PYTHON.SRC)\
	)))

.PHONY: check
check: $(PYTHON.UNITTEST_STAMPS)

$(PYTHON.UNITTEST_STAMPS): stamps/%.unittest: %.py
	python -m unittest $(subst /,.,$*)
	@mkdir -p $(@D)
	@touch $@


PYTHON.PYLINT_STAMPS := $(strip \
	$(patsubst %.py,stamps/%.pylint,\
	$(filter-out %__init__.py,\
	$(PYTHON_SRC)\
	)))

.PHONY: pylint
pylint: $(PYTHON.PYLINT_STAMPS)

$(PYTHON.PYLINT_STAMPS): stamps/%.pylint: %.py
	@mkdir -p $(@D)
	-pylint $< > $@
	cat $@


.PHONY: uml
uml:
	pyreverse -ASmy -k -o png $(PYTHON_SRC) -p $(patsubst %.py,%,$(PYTHON.MAIN))


#############################


#############################
.PHONY: run
run: python-run

.PHONY: python-run
python-run:
	python $(PYTHON.MAIN)
#############################
