import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb.result import TestFailure


@cocotb.test()
async def test_dff(dut):
    """Testing dff for reset """

    clock = Clock(dut.c, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.d.value = 1

    dut.res.value = 0
    await RisingEdge(dut.c)
    await RisingEdge(dut.c)
    
    assert dut.q.value == 0, f"Reset failure {dut.q.value} != {dut.d.value}"

    dut.res.value = 1

    await RisingEdge(dut.c)
    await RisingEdge(dut.c)

    assert dut.q.value == dut.d.value, f"Reset failure {dut.q.value} != {dut.d.value}"

