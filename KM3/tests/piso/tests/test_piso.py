import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import random

async def reset_dut(dut, duration_ns=10):
    dut.reset.value = 1
    dut.load.value = 0
    dut.p_in.value = 0
    await Timer(duration_ns, units="ns")
    dut.reset.value = 0
    await RisingEdge(dut.clk)

async def load_parallel_data(dut, data):
    dut.load.value = 1
    dut.p_in.value = data
    await RisingEdge(dut.clk)
    dut.load.value = 0

@cocotb.test()
async def test_piso_serial_output(dut):
    """Test PISO: Load parallel data and check serial output"""

    WIDTH = len(dut.p_in)  # Automatically get width from DUT
    test_data = random.randint(0, 2**WIDTH - 1)
    expected_bits = [(test_data >> i) & 1 for i in range(WIDTH)]

    # Start clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz
    cocotb.start_soon(clock.start())

    # Apply reset
    await reset_dut(dut)

    # Load parallel data
    await load_parallel_data(dut, test_data)

    # Wait for and check each bit
    for expected_bit in expected_bits:
        await RisingEdge(dut.clk)
        assert dut.s_out.value == expected_bit, \
            f"At bit, expected {expected_bit}, got {int(dut.s_out.value)}"

@cocotb.test()
async def test_piso_reset_behavior(dut):
    """Test that reset clears output and register"""

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Set some initial values
    await load_parallel_data(dut, 0b10101010)

    # Reset
    await reset_dut(dut)

    # After reset, s_out should not be latched from reg_out
    await RisingEdge(dut.clk)
    assert dut.s_out.value == 0, "After reset, s_out should be 0"
    # Additional checks can be done if internal reg_out is visible (add it to `output` in DUT)

