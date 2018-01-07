class Transition:
    def __init__(self, symbols, new_state):
        self.symbols = symbols
        self.new_state = new_state


class State:
    def __init__(self, label, starting=False, final=False):
        self.label = label
        self.starting = starting
        self.final = final
        self.transitions = []


class FiniteAutomaton:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.states = {}
        self.states_to_process = {}

    def add_state(self, state):
        label = state.label
        if label in self.states_to_process:
            del self.states_to_process[label]
        self.states[label] = state

    def create_and_add_state(self, label, starting=False, final=False):
        if label in self.states_to_process:
            del self.states_to_process
        self.states[label] = State(label, starting, final)

    def add_transition(self, symbols, source, destination):
        if source in self.states_to_process:
            del self.states_to_process[source]
        for symbol in symbols:
            for char in symbol:
                if char not in self.alphabet:
                    raise RuntimeError
        if destination not in self.states:
            self.states_to_process[destination] = True
            self.states[destination] = State(destination, False, False)
        self.states[source].transitions.append(Transition(symbols, destination))

    def process(self, text, position):
        queue = [(None, '', position)]
        valid_text = ''
        while len(queue):
            current_state = queue.pop(0)
            current_index = current_state[2]
            if current_state[0] and current_state[0].final and len(current_state[1]) > len(valid_text):
                valid_text = current_state[1]
            if current_state[0] is None:
                for state in [s for s in self.states.values() if s.starting]:
                    for transition in state.transitions:
                        for symbol in transition.symbols:
                            if text[current_index: current_index + len(symbol)] == symbol:
                                queue.append(
                                    (self.states[transition.new_state],
                                     current_state[1] + symbol,
                                     current_index + len(symbol)))
            else:
                for transition in current_state[0].transitions:
                    for symbol in transition.symbols:
                        if text[current_index: current_index + len(symbol)] == symbol:
                            queue.append(
                                (self.states[transition.new_state],
                                 current_state[1] + symbol,
                                 current_index + len(symbol)))
        return valid_text, position + len(valid_text)
