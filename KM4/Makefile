SIM ?= icarus

TOPLEVEL_LANG ?= verilog

VERILOG_DIRS = ./rtl
RTL_FILEPATHS = $(foreach d, $(VERILOG_DIRS), $(wildcard $(addprefix $(d)/*,*.v)))
VERILOG_SOURCES += $(RTL_FILEPATHS)

TOPLEVEL ?= Bus 

MODULE ?= test_m2  

export PYTHONPATH=$(shell pwd)/tests

include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: clean

clean::
	rm -rf __pycache__ sim_build results.xml tests/__pycache__
