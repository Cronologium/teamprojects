import json

from lexical_analyser.automaton.automaton_parser import FiniteAutomatonParser, AutomatonException
from lexical_analyser.automaton.finite_automaton import FiniteAutomaton, State


class FiniteJsonAutomatonParser(FiniteAutomatonParser):
    def __init__(self):
        super()

    def parse(self, filename=None):
        if filename is None:
            raise AutomatonException

        automaton_json = json.load(open(filename, 'r'))
        finite_automaton = FiniteAutomaton(automaton_json['alphabet'])
        for state in automaton_json['states']:
            finite_automaton.add_state(State(state['label'], state['starting'], state['final']))
            for transition in state['transitions']:
                finite_automaton.add_transition(transition['symbols'], state['label'], transition['new_state'])
        if len(finite_automaton.states_to_process):
            raise AutomatonException
        if len(str([state for state in finite_automaton.states.keys() if finite_automaton.states[state].final])) == 0:
            raise AutomatonException
        if len(str([state for state in finite_automaton.states.keys() if
                    finite_automaton.states[state].starting])) == 0:
            raise AutomatonException
        return finite_automaton
