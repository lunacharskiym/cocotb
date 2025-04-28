import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb.result import TestFailure


@cocotb.test()
async def test_counter8bit(dut):
    """Testing counter for reset and counting"""

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.reset.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.reset.value = 0

    await RisingEdge(dut.clk)

    assert dut.o_count.value == 0, f"After reset, o_count={dut.o_count.value}"

    for expected_count in range(1, 260):

        await RisingEdge(dut.clk)        

        actual_count = dut.o_count.value.integer
        expected_mod = expected_count % 256
        
        assert actual_count == expected_mod, f"At {expected_count} clk, expected {expected_mod}, got {actual_count}"

    dut._log.info("Test completed")
