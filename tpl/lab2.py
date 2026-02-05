from collections import deque, defaultdict

class FiniteStateMachine:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = set(final_states)

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), [])
                if len(next_states) > 1:
                    return False
        return True

    def to_dfa(self):
        dfa_transitions = {}
        dfa_start_state = frozenset([self.start_state])
        dfa_states = set([dfa_start_state])
        dfa_final_states = set()
        queue = deque([dfa_start_state])
        
        while queue:
            current_set = queue.popleft()
            for symbol in self.alphabet:
                next_set = set()
                for state in current_set:
                    next_set.update(self.transitions.get((state, symbol), []))
                next_set = frozenset(next_set)
                if next_set:
                    dfa_transitions[(current_set, symbol)] = next_set
                    if next_set not in dfa_states:
                        dfa_states.add(next_set)
                        queue.append(next_set)
                if any(state in self.final_states for state in next_set):
                    dfa_final_states.add(next_set)
        
        dfa = FiniteStateMachine(
            [frozenset(s) for s in dfa_states],
            self.alphabet,
            {k: [v] for k, v in dfa_transitions.items()},
            dfa_start_state,
            dfa_final_states
        )
        return dfa.remove_unreachable_states()

    def remove_unreachable_states(self):
        reachable = set()
        queue = deque([self.start_state])
        while queue:
            state = queue.popleft()
            if state in reachable:
                continue
            reachable.add(state)
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), [])
                for next_state in next_states:
                    if next_state not in reachable:
                        queue.append(next_state)
        
        new_states = reachable
        new_final_states = self.final_states & reachable # пересечение финальных состояний с достижимыми состояниями
        new_transitions = {}
        for (state, symbol), next_states in self.transitions.items():
            if state in reachable:
                new_next_states = [s for s in next_states if s in reachable]
                if new_next_states:
                    new_transitions[(state, symbol)] = new_next_states
        
        return FiniteStateMachine(
            new_states,
            self.alphabet,
            new_transitions,
            self.start_state,
            new_final_states
        )

    def minimize(self):
        if not self.is_deterministic():
            dfa = self.to_dfa()
        else:
            dfa = self.remove_unreachable_states()
        
        P = [dfa.final_states, dfa.states - dfa.final_states]
        P = [s for s in P if s]
        W = deque(P)
        
        while W:
            A = W.popleft()
            for c in dfa.alphabet:
                X = set()
                for state in dfa.states:
                    next_states = dfa.transitions.get((state, c), [])
                    if next_states and next_states[0] in A:
                        X.add(state)
                for Y in P[:]:
                    intersect = X & Y
                    difference = Y - X
                    if intersect and difference:
                        P.remove(Y)
                        P.append(intersect)
                        P.append(difference)
                        if Y in W:
                            W.remove(Y)
                            W.append(intersect)
                            W.append(difference)
                        else:
                            if len(intersect) <= len(difference):
                                W.append(intersect)
                            else:
                                W.append(difference)
        
        state_to_class = {}
        for i, equiv_class in enumerate(P):
            for state in equiv_class:
                state_to_class[state] = i
        
        new_states = set(state_to_class.values())
        new_start_state = state_to_class[dfa.start_state]
        new_final_states = {state_to_class[state] for state in dfa.final_states}
        new_transitions = {}
        
        for (state, symbol), next_states in dfa.transitions.items():
            if next_states:
                new_state = state_to_class[state]
                new_next = state_to_class[next_states[0]]
                new_transitions[(new_state, symbol)] = [new_next]
        
        return FiniteStateMachine(
            new_states,
            dfa.alphabet,
            new_transitions,
            new_start_state,
            new_final_states
        )

    def __repr__(self):
        return (f"FSM(States: {self.states}, Alphabet: {self.alphabet}, "
                f"Start: {self.start_state}, Final: {self.final_states}\n"
                f"Transitions: {self.transitions})")


states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
alphabet = ['0', '1']
transitions = {
    ('q0', '0'): ['q1'],
    ('q0', '1'): ['q2'],
    ('q1', '0'): ['q4'],
    ('q1', '1'): ['q2'],
    ('q2', '0'): ['q3'],
    ('q2', '1'): ['q0'],
    ('q3', '0'): ['q5'],
    ('q3', '1'): ['q2'],
    ('q4', '0'): ['q5'],
    ('q4', '1'): ['q5'],
    ('q5', '0'): ['q4'],
    ('q5', '1'): ['q4'],
}
start_state = 'q0'
final_states = ['q4', 'q5']

fsm = FiniteStateMachine(states, alphabet, transitions, start_state, final_states)
minimized_fsm = fsm.minimize()
print(minimized_fsm)