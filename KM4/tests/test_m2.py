import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge

outputs_model = {
'gnt1'          :     'x',
'gnt2'          :     'x',
'sb_masters'    :   2*'x',
'sb_mastlock'   :     'x',
'RDATA'         :  32*'z',
'HADDR'         :  14*'z',
'sel_0'         :  0b1   ,
'sel_1'         :     'x',
'sel_2'         :     'x',
'sel_slave'     :  0b0   ,
'WDATA'         :  32*'z',
}

outputs_result = outputs_model.copy()

def readOutputs (outputs_result, dut):
    for key in outputs_result.keys():
        pinObject = getattr(dut,key)

        if type (outputs_model[key]) == str:
            outputs_result[key] = str(pinObject.value)
        else:
            outputs_result[key] = pinObject.value
    return outputs_result            


@cocotb.test()
async def test_m2(dut):
    """Проверка сброса шины"""
    cocotb.start_soon(Clock(dut.clk,2,units="ns").start())
    dut.rst.value = 0
    await FallingEdge(dut.clk)
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    outputs_model.update({
        'gnt1'         : 0b0,
        'gnt2'         : 0b0,
        'sb_masters'   : 0b0,
        'sb_mastlock'  : 0b0,
    })
        # запрос без блокировки шины
    await RisingEdge(dut.clk)
    dut.HADDR_M2.value = 0b01010011110011 
    dut.RDATA_S0.value = 11
    dut.RDATA_S1.value = 3137
    dut.RDATA_S2.value = 335811
    dut.WDATA_M2 = 24457
    dut.sb_lock_m2.value = 0
    dut.req2.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model.update({
        'gnt1'         : 0b0,
        'gnt2'         : 0b1,
        'sb_masters'   : 0b10,
        'sb_mastlock'  : 0b0,
        'RDATA'        : 0b00000000000000000000110001000001,
        'HADDR'        : 0b01010011110011,
        'sel_0'        : 0b0,
        'sel_1'        : 0b1,
        'sel_2'        : 0b0,
        'sel_slave'    : 0b01,
        'WDATA'        : 0b00000000000000000101111110001001,
    })
    await ClockCycles(dut.clk, 1)

    readOutputs (outputs_result, dut)
    print ("")
    print ("Одиночный запрос без блокировки шины")
    for key in outputs_result:
        print(f"{key:<15}: {outputs_result[key]}")
    print ("")

    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString 
    
    # запрос к разным ведомым 
    await RisingEdge(dut.clk)
    dut.HADDR_M2.value = 0b00010011110011 
    dut.sb_lock_m2.value = 0
    dut.req2.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model.update({
        'RDATA'        : 0b00000000000000000000000000001011,
        'HADDR'        : 0b00010011110011,
        'sel_0'        : 0b1,
        'sel_1'        : 0b0,
        'sel_slave'    : 0b0,
    })
    readOutputs (outputs_result, dut)
    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString

    await RisingEdge(dut.clk )
    dut.HADDR_M2.value = 0b10010011110011 
    dut.sb_lock_m2.value = 0
    dut.req2.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model.update({
        'RDATA'        : 0b00000000000001010001111111000011,
        'HADDR'        : 0b10010011110011,
        'sel_0'        : 0b0,
        'sel_2'        : 0b1,
        'sel_slave'    : 0b10,
    })
    readOutputs (outputs_result, dut)
    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString    

    # запрос с блокировкой шины 
    await RisingEdge(dut.clk)
    dut.sb_lock_m2.value = 1
    dut.req2.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model['sb_mastlock']  = 0b0    
    readOutputs (outputs_result, dut)
    print ("")
    print ("Одиночный запрос с блокировкой шины")
    for key in outputs_result:
        print(f"{key:<15}: {outputs_result[key]}")
    print ("") 

    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString

@cocotb.test()
async def test_m1(dut):
    """Проверка сброса шины"""
    cocotb.start_soon(Clock(dut.clk,2,units="ns").start())
    dut.rst.value = 0
    await FallingEdge(dut.clk)
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    outputs_model.update({
        'gnt1'         : 0b0,
        'gnt2'         : 0b0,
        'sb_masters'   : 0b0,
        'sb_mastlock'  : 0b0,
    })
        # запрос без блокировки шины
    await RisingEdge(dut.clk)
    dut.HADDR_M1.value = 0b01010011110011 
    dut.RDATA_S0.value = 11
    dut.RDATA_S1.value = 3137
    dut.RDATA_S2.value = 335811
    dut.WDATA_M1 = 24457
    dut.sb_lock_m1.value = 1
    dut.req1.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model.update({
        'gnt1'         : 0b1,
        'gnt2'         : 0b0,
        'sb_masters'   : 0b01,
        'sb_mastlock'  : 0b1,
        'RDATA'        : 0b00000000000000000000110001000001,
        'HADDR'        : 0b01010011110011,
        'sel_0'        : 0b0,
        'sel_1'        : 0b1,
        'sel_2'        : 0b0,
        'sel_slave'    : 0b01,
        'WDATA'        : 0b00000000000000000101111110001001,
    })
    await ClockCycles(dut.clk, 1)

    readOutputs (outputs_result, dut)
    print ("")
    print ("Одиночный запрос без блокировки шины")
    for key in outputs_result:
        print(f"{key:<15}: {outputs_result[key]}")
    print ("")

    for key in outputs_model:
        AssertionString = f"{key}: Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString 
    
    # запрос к разным ведомым 
    await RisingEdge(dut.clk)
    dut.HADDR_M1.value = 0b00010011110011 
    dut.sb_lock_m1.value = 0
    dut.req1.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model.update({
        'RDATA'        : 0b00000000000000000000000000001011,
        'HADDR'        : 0b00010011110011,
        'sel_0'        : 0b1,
        'sel_1'        : 0b0,
        'sel_slave'    : 0b0,
    })
    readOutputs (outputs_result, dut)
    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString

    await RisingEdge(dut.clk )
    dut.HADDR_M1.value = 0b10010011110011 
    dut.sb_lock_m2.value = 0
    dut.req2.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model.update({
        'RDATA'        : 0b00000000000001010001111111000011,
        'HADDR'        : 0b10010011110011,
        'sel_0'        : 0b0,
        'sel_2'        : 0b1,
        'sel_slave'    : 0b10,
    })
    readOutputs (outputs_result, dut)
    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString    

    # запрос с блокировкой шины 
    await RisingEdge(dut.clk)
    dut.sb_lock_m2.value = 1
    dut.req2.value = 1
    await ClockCycles(dut.clk, 2)
    outputs_model['sb_mastlock']  = 0b0    
    readOutputs (outputs_result, dut)
    print ("")
    print ("Одиночный запрос с блокировкой шины")
    for key in outputs_result:
        print(f"{key:<15}: {outputs_result[key]}")
    print ("") 

    for key in outputs_model:
        AssertionString = f"Ожидали {outputs_model[key]} а получили {outputs_result[key]} "
        assert outputs_result[key] == outputs_model[key] , AssertionString

