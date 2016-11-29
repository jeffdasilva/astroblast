###############################################################################
#
# Jeff DaSilva
# Copyright 2016 All Rights Reserved
#
###############################################################################

ENABLE_GIT := 1
ENABLE_PYTHON := 1

include bcommon/inc.mk

ifeq ($(DEBUG),1)
$(info Done reading inc.mk)
endif


.PHONY: test
test:
	PYTHONPATH=$(abspath .) python ./tests/nios2/nios2simple.py
	$(MAKE) -C work/tests/nios2/simple