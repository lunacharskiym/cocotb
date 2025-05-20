from transitions import Machine
from transitions.extensions import GraphMachine


state_array = ["Start", "Position1", "Position2", "Position3", "End",]
transition_array = [
        {'trigger':'Position1', 'source':'Start',   'dest':'Position1'},
        {'trigger':'Position2', 'source':'Start',   'dest':'Position2'},
        {'trigger':'Position3', 'source':'Start',   'dest':'Position3'},

        {'trigger':'reset',     'source':'Position1, Position2, Position3',   'dest':'Start'},
        {'trigger':'hold',      'source':'Position1, Position2, Position3',   'dest':'Position1, Position2, Position3'},
]

class FSM_Class():
    pass

test_FSM = FSM_Class()

graph_machine = GraphMachine(model=test_FSM, 
                             states=state_array,
                             transitions=transition_array, 
                             initial="Start", 
                             title='TestFsm')


# machine = Machine(model=test_FSM, 
#                          states=stateArray,
#                          transitions=transition_array, 
#                          initial="Start")

test_FSM.get_graph().draw('start.svg', prog='dot')


