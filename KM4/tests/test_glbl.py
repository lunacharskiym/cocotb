import cocotb
from cocotb.triggers import FallingEdge,RisingEdge, ClockCycles
from cocotb.clock import Clock
from cocotb.binary import BinaryValue

outputs_model = {
    'gnt1': 'x',
    'gnt2': 'x',
    'sb_masters': 'xx',
    'sb_mastlock': 'x',
    'RDATA': 32 * 'z',
    'HADDR': 14 * 'z',
    'sel_0': '1',
    'sel_1': 'x',
    'sel_2': 'x',
    'sel_slave': '00',
    'WDATA': 32 * 'z',
}


def read_outputs(dut):
    result = {}
    for key, expected in outputs_model.items():
        pin = getattr(dut, key)
        result[key] = str(pin.value) if isinstance(expected, str) else pin.value
    return result

def check_outputs(dut, expected_model):

    result = read_outputs(dut)

    for key in result:
        assert result[key] == expected_model[key], f"{key}: expected {expected_model[key]}, got {result[key]}"

async def initialize_dut(dut):
    cocotb.start_soon(Clock(dut.clk, 2, units="ns").start())
    dut.rst.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 1

@cocotb.test()
async def test_reset(dut):
    """Проверка сброса"""
    await initialize_dut(dut)
    check_outputs(dut, outputs_model)

    expected = outputs_model.copy()
    expected.update({
        'gnt1': '0',
        'gnt2': '0',
        'sb_masters': '00',
        'sb_mastlock': '0',
    })
    await ClockCycles(dut.clk, 2)
    check_outputs(dut, expected)

@cocotb.test()
async def test_master1_request_no_lock(dut):
    """Одиночный запрос от master1 без блокировки"""
    await initialize_dut(dut)

    dut.req1.value = 0
    dut.req2.value = 0
    dut.sb_lock_m1.value = 0
    dut.sb_lock_m2.value = 0
    dut.sb_split_ar.value = 0
    dut.resp.value = 0

    await RisingEdge(dut.clk)

    dut.req1.value = 1 
    dut.req2.value = 0 
    dut.HADDR_M1.value = BinaryValue(0x000F, n_bits=14)
    dut.WDATA_M1.value =  BinaryValue(0xABCD1234, n_bits=32)

    for i in range(20):
        await ClockCycles(dut.clk, 1)
        dut._log.info(f"Cycle {i}: gnt1={dut.gnt1.value}, gnt2={dut.gnt2.value}, sb_masters={dut.sb_masters.value}")
        dut._log.info(f"req1={dut.req1.value}, req2={dut.req2.value}")

    
    expected = outputs_model.copy()
    expected.update({
        'gnt1': '1',
        'gnt2': '0',
        'sb_masters': '00',
        'sb_mastlock': '0',
        'HADDR': str(BinaryValue(0x000F, n_bits=14)),
        'WDATA': str(BinaryValue(0xABCD1234, n_bits=32)),
    })
    check_outputs(dut, expected)

# @cocotb.test()
# async def test_master1_request_with_lock(dut):
#     """Одиночный запрос от master1 с блокировкой"""
#     await initialize_dut(dut)
# 
#     dut.req1.value = 1
#     dut.sb_lock_m1.value = 1
#     dut.HADDR_M1.value = 0x2000
#     dut.WDATA_M1.value = 0x12345678
# 
#     await ClockCycles(dut.clk, 2)
# 
#     expected = outputs_model.copy()
#     expected.update({
#         'gnt1': 1,
#         'gnt2': 0,
#         'sb_masters': 0b01,
#         'sb_mastlock': 1,
#         'HADDR': 0x2000,
#         'WDATA': 0x12345678,
#     })
#     check_outputs(dut, expected)
 
@cocotb.test()
async def test_master2_request_no_lock(dut):
    """Одиночный запрос от master2 без блокировки"""
    await initialize_dut(dut)

    dut.req1.value = 0
    dut.req2.value = 0
    dut.sb_lock_m1.value = 0
    dut.sb_lock_m2.value = 0
    dut.sb_split_ar.value = 0
    dut.resp.value = 0

    await RisingEdge(dut.clk)

    dut.req1.value = 0 
    dut.req2.value = 1 
    dut.HADDR_M1.value = BinaryValue(0x000F, n_bits=14)
    dut.WDATA_M1.value =  BinaryValue(0xABCD1234, n_bits=32)

    for i in range(20):
        await ClockCycles(dut.clk, 1)
        dut._log.info(f"Cycle {i}: gnt1={dut.gnt1.value}, gnt2={dut.gnt2.value}, sb_masters={dut.sb_masters.value}")
        dut._log.info(f"req1={dut.req1.value}, req2={dut.req2.value}")

    
    expected = outputs_model.copy()
    expected.update({
        'gnt1': '0',
        'gnt2': '1',
        'sb_masters': '10',
        'sb_mastlock': '0',
        'HADDR': str(BinaryValue(0x000F, n_bits=14)),
        'WDATA': str(BinaryValue(0xABCD1234, n_bits=32)),
    })
    check_outputs(dut, expected)
 
@cocotb.test()
async def test_both_masters_conflict_same_slave(dut):
    """Оба ведущих делают запрос к одному и тому же ведомому"""
    await initialize_dut(dut)

    dut.req1.value = 1
    dut.HADDR_M1.value = 0x2001  # адрес ведомого 0

    dut.req2.value = 1
    dut.HADDR_M2.value = 0x2001 # тот же ведомый
 
    await ClockCycles(dut.clk, 2)
 
    expected = outputs_model.copy()
    expected.update({
        'gnt1': 1,
        'gnt2': 0,
        'sb_masters': 0b01,
        'sb_mastlock': 0,
        'HADDR': 0x2001,
    })
    check_outputs(dut, expected)

# @cocotb.test()
# async def test_both_masters_different_slaves(dut):
#     """Оба ведущих делают запросы к разным ведомым"""
#     await initialize_dut(dut)
# 
#     dut.req1.value = 1
#     dut.HADDR_M1.value = 0x1000  # ведомый 0
# 
#     dut.req2.value = 1
#     dut.HADDR_M2.value = 0x2002  # ведомый 1
# 
#     await ClockCycles(dut.clk, 2)
# 
#     result = read_outputs(dut)
#     assert (result['gnt1'] == 1 or result['gnt2'] == 1), "Ожидался хотя бы один gnt=1"
#     assert result['sb_mastlock'] == 0
#     assert result['HADDR'] in (0x1000, 0x2002)

