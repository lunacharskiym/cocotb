
import pytest
from model import test_FSM  # Импорт твоего FSM-объекта из файла model.py

def setup_function():
    # Сброс FSM перед каждым тестом (если он не в Start, вызвать reset)
    if test_FSM.state != 'Start':
        if hasattr(test_FSM, 'reset'):
            try:
                test_FSM.reset()
            except:
                pass  # если состояние не допускает reset
        else:
            # Принудительно сбросить состояние (если нужно)
            test_FSM.state = 'Start'

def test_initial_state():
    assert test_FSM.state == 'Start'

def test_position1_transition():
    test_FSM.Position1()
    assert test_FSM.state == 'Position1'

def test_position2_transition():
    test_FSM.Position2()
    assert test_FSM.state == 'Position2'

def test_position3_transition():
    test_FSM.Position3()
    assert test_FSM.state == 'Position3'

def test_hold_transition_from_position1():
    test_FSM.Position1()
    test_FSM.hold()
    assert test_FSM.state == 'Position1'

def test_reset_from_position2():
    test_FSM.Position2()
    test_FSM.reset()
    assert test_FSM.state == 'Start'

def test_hold_transition_from_position3():
    test_FSM.Position3()
    test_FSM.hold()
    assert test_FSM.state == 'Position3'
