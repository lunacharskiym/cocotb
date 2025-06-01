SIM ?= icarus

TOPLEVEL_LANG ?= verilog

TESTDIR ?= counter8bit

VERILOG_SOURCES ?= $(wildcard $(TESTDIR)/rtl/*.v $(TESTDIR)/rtl/*.sv) 

TOPLEVEL ?= $(TESTDIR)

MODULE ?= test_$(TOPLEVEL)

export PYTHONPATH=$(TESTDIR)/tests

include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: clean

clean::
	rm -rf __pycache__ sim_build results.xml $(TESTDIR)/tests/__pycache__
