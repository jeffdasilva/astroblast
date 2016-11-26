###############################################################################
#
# Jeff DaSilva
# Copyright 2016 All Rights Reserved
#
###############################################################################

ifeq ($(DEBUG),1)
$(info inc.mk included)
endif

#############################
THIS_INC_MK_MAKEFILE :=  $(abspath $(lastword $(MAKEFILE_LIST)))
THIS_INC_MK_DIR := $(patsubst %/,%,$(dir $(THIS_INC_MK_MAKEFILE)))

.SECONDEXPANSION:
SHELL := /bin/bash

SPACE := $(empty) $(empty)

define tolower
$(strip \
$(subst A,a,\
$(subst B,b,\
$(subst C,c,\
$(subst D,d,\
$(subst E,e,\
$(subst F,f,\
$(subst G,g,\
$(subst H,h,\
$(subst I,i,\
$(subst J,j,\
$(subst K,k,\
$(subst L,l,\
$(subst M,m,\
$(subst N,n,\
$(subst O,o,\
$(subst P,p,\
$(subst Q,q,\
$(subst R,r,\
$(subst S,s,\
$(subst T,t,\
$(subst U,u,\
$(subst V,v,\
$(subst W,w,\
$(subst X,x,\
$(subst Y,y,\
$(subst Z,z,\
$1 \
)))))))))))))))))))))))))))
endef

define toupper
$(strip \
$(subst a,A,\
$(subst b,B,\
$(subst c,C,\
$(subst d,D,\
$(subst e,E,\
$(subst f,F,\
$(subst g,G,\
$(subst h,H,\
$(subst i,I,\
$(subst j,J,\
$(subst k,K,\
$(subst l,L,\
$(subst m,M,\
$(subst n,N,\
$(subst o,O,\
$(subst p,P,\
$(subst q,Q,\
$(subst r,R,\
$(subst s,S,\
$(subst t,T,\
$(subst u,U,\
$(subst v,V,\
$(subst w,W,\
$(subst x,X,\
$(subst y,Y,\
$(subst z,Z,\
$1 \
)))))))))))))))))))))))))))
endef

ifneq ($(COMSPEC),)
UNAME_O := Msys
else
UNAME_O := $(shell uname -o)
endif

HOST_OS := $(call tolower,$(UNAME_O))

ifeq ($(HOST_OS),msys)
IS_WINDOWS_HOST_OS := 1
endif
ifeq ($(HOST_OS),cygwin)
IS_WINDOWS_HOST_OS := 1
endif

ifeq ($(DEBUG),1)
$(info HOST_OS is $(HOST_OS))
endif
#############################


#############################
.PHONY: default
default: $(if $(DEFAULT_TARGET),$(DEFAULT_TARGET),check)

.PHONY: all
.PHONY: check
.PHONY: run
.PHONY: test

check: all
test: check
#############################


#############################
PLUGINS_AVAILABLE := $(filter-out inc,$(patsubst $(THIS_INC_MK_DIR)/%.mk,%,$(wildcard $(THIS_INC_MK_DIR)/*.mk)))
PLUGINS_ENABLED := $(foreach plugin,$(PLUGINS_AVAILABLE),$(if $(ENABLE_$(call toupper,$(plugin))),$(plugin)))
include $(patsubst %,$(THIS_INC_MK_DIR)/%.mk,$(PLUGINS_ENABLED))
#############################


#############################
.PHONY: tabs2space
tabs2space:
	@find . -type f -name '*.py' -exec sed -i 's/\t/    /g' {} \;

.PHONY: remove-trailing-whitespace
remove-trailing-whitespace:
	@find . -type f -name '*.py' -exec sed -i 's/[ \t]*$$//g' {} \;

.PHONY: remove-windows-line-endings
remove-windows-line-endings:
ifneq ($(IS_WINDOWS_HOST_OS),1)
ifeq ($(shell which dos2unix 2>/dev/null),)
	$(warning WARNING: dos2unix not installed)
	@sleep 2
else 
	@find . -type f \( -name '*.py' -o -name 'Makefile' -o -name '*.mk' -o -name '*.md' -o -name 'LICENSE' \) \
		-exec dos2unix {} \;
endif
endif

.PHONY: lint
#lint: increment-build-number
lint: remove-trailing-whitespace remove-windows-line-endings tabs2space
	$(MAKE) check
	$(MAKE) clean
#############################

#############################
CURRENT_BUILD_NUMBER = $(shell grep "BuildNumber = [0-9]*$$" $(PYTHON.MAIN) | head -n1 | sed -e 's,.*=[ \t]*,,g')
NEXT_BUILD_NUMBER = $(shell echo $$[$(CURRENT_BUILD_NUMBER)+1])

.PHONY: increment-build-number
increment-build-number:
ifeq ($(notdir $(shell whoami)),jdasilva)
	@echo "Incrementing build number to: $(NEXT_BUILD_NUMBER)"
	@sed -i -e 's,\(BuildNumber = \)\([0-9]*\)$$,\1$(NEXT_BUILD_NUMBER),g' $(PYTHON.MAIN)
endif

CURRENT_MINOR_VERSION_NUMBER = $(shell grep "MinorVersion = [0-9]*$$" $(PYTHON.MAIN) | head -n1 | sed -e 's,.*=[ \t]*,,g')
NEXT_MINOR_VERSION_NUMBER = $(shell echo $$[$(CURRENT_MINOR_VERSION_NUMBER)+1])

.PHONY: increment-minor-version
increment-minor-version:
ifeq ($(notdir $(shell whoami)),jdasilva)
	@echo "Incrementing minor version number to: $(NEXT_MINOR_VERSION_NUMBER)"
	@sed -i -e 's,\(MinorVersion = \)\([0-9]*\)$$,\1$(NEXT_MINOR_VERSION_NUMBER),g' $(PYTHON.MAIN)
endif
#############################

#############################
CLEAN_FILES_RE += *.pyc *.class stamps test*.pickle *.orig *~ *.png
CLEAN_FILES += $(sort $(wildcard $(strip \
	$(foreach dir,. $(PYTHON.PACKAGES),\
	$(foreach clean_re,$(CLEAN_FILES_RE), \
		$(dir)/$(clean_re) \
)))) \
$(wildcard work) \
)

.PHONY: clean
clean:
	$(if $(strip $(CLEAN_FILES)),rm -rf $(CLEAN_FILES))

TARBALL_TIMESTAMP := $(strip $(subst $(SPACE),,$(shell date +%m%d%Y_%k%M%S)))
TARBALL_FILE := tgz/$(notdir $(abspath .))_$(TARBALL_TIMESTAMP).tar.gz

.PHONY: archive tarball tgz
archive tarball tgz: $(TARBALL_FILE)

$(TARBALL_FILE): clean
	@mkdir -p $(@D)
	@echo "Generating $@..."
	tar -czf $@ $(filter-out tgz,$(wildcard *))
#############################
