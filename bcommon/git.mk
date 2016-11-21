###############################################################################
#
# Jeff DaSilva
# Copyright 2016 All Rights Reserved
#
###############################################################################

ifeq ($(DEBUG),1)
$(info git.mk included)
endif

GIT.PUSH_DEPS = increment-minor-version
