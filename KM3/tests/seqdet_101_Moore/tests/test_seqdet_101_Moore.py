import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from cocotb.result import TestFailure


@cocotb.test()
async def test_seqdet_101_moore(dut):
    """ Testing 101 sequence detector """

    # initialization
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    
    dut.rst.value = 0
    dut.x.value = 0

    await Timer(15, units="ns")
    dut.rst.value = 1;
    await RisingEdge(dut.clk)
    
    output = await send_bitstream(dut, [1, 0, 1, 0,])
    assert output == [0, 0, 0, 1], f"Failed to detect '101' : got {output}"

    dut.rst.value = 0
    await RisingEdge(dut.clk)
    dut.rst.value = 1
    await RisingEdge(dut.clk)

    output = await send_bitstream(dut, [1, 1, 0, 1, 0])
    assert output == [0, 0, 0, 0, 0], f"Incorrect output for invalid sequence: got {output}"

    output = await send_bitstream(dut, [1, 0, 1, 0, 1, 0])
    assert output == [0, 0, 0, 1, 0, 0], f"Overlapping sequence failed: got {output}"


async def send_bitstream(dut, bitstream):
    outputs = []
    for bit in bitstream:
        dut.x.value = bit
        await RisingEdge(dut.clk)
        outputs.append(int(dut.y.value))

    await RisingEdge(dut.clk)

    return outputs
