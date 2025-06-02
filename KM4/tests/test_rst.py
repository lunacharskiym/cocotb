import cocotb
from cocotb.triggers import Timer, ClockCycles, FallingEdge
from cocotb.clock import Clock

outputs_model = {
    'gnt1'          :   'x',
    'gnt2'          :   'x',
    'sb_masters'    :2* 'x',
    'sb_mastlock'   :   'x',
    'RDATA'         :32*'z',
    'HADDR'         :14*'z',
    'sel_0'         :0b1   ,
    'sel_1'         :   'x',
    'sel_2'         :   'x',
    'sel_slave'     :0b00  ,
    'WDATA'         :32*'z',
}

outputs_result = outputs_model.copy()

def read_outputs(outputs_result, dut):

    for key in outputs_result.keys():

        pin_object = getattr(dut, key)

        if type(outputs_model[key]) == str:
            outputs_result[key] = str(pin_object.value)
        else:
            outputs_result[key] = pin_object.value
    
    return outputs_result

@cocotb.test()
async def test(dut):
    """Reset check"""
    cocotb.start_soon(Clock(dut.clk, 2, units="ns").start())
    dut.rst.value = 0
    
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    read_outputs(outputs_result, dut)

    print("\nAfter reset")
    for key in outputs_result:
        print(f"{key:<15}: {outputs_result[key]}")
    print(" ")


    assert outputs_result == outputs_model

    outputs_model['gnt1'] = 0b0
    outputs_model['gnt2'] = 0b0
    outputs_model['sb_masters'] = 0b00
    outputs_model['sb_mastlock'] = 0b0

    await ClockCycles(dut.clk, 1)

    read_outputs(outputs_result, dut)

    print("\nAfter reset and clock")
    for key in outputs_result:
        print(f"{key:<15}: {outputs_result[key]}")
    print(" ")

    for key in outputs_result:
        assertion_string = f"Expected {outputs_model[key]}, but got {outputs_result[key]}"
        assert outputs_result[key] == outputs_model[key], assertion_string

