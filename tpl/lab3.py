class DPDA:
    def __init__(self, transitions, start_state, start_stack, final_states):
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack = start_stack
        self.final_states = final_states

    def accepts(self, input_string):
        '''Проверяет, принадлежит ли цепочка языку автомата.'''
        state = self.start_state
        stack = [self.start_stack]
        index = 0
        
        max_steps = 1000
        step_count = 0
        
        while step_count < max_steps:
            step_count += 1
            
            if index == len(input_string):
                # Проверка допускающего состояния
                if state in self.final_states:
                    return True, "Цепочка проходит"
                if self._try_epsilon_transition(state, stack):
                    continue
                return False, "Цепочка не проходит"
            
            current_char = input_string[index]
            transition_result = self._try_transition(state, current_char, stack)
            if transition_result[0]:
                state = transition_result[1]
                index += 1
                continue
            
            epsilon_result = self._try_epsilon_transition(state, stack)
            if epsilon_result[0]:
                state = epsilon_result[1]
                continue
            
            # Если нет возможных переходов
            remaining_input = input_string[index:]
            return False, f"Нет перехода для символа '{current_char}' в состоянии {state} при элементе в стеке {stack[-1] if stack else 'пустой стек'}. Остаток: {remaining_input}"
        
        return False, "Превышено максимальное количество шагов - возможен бесконечный цикл"

    def _try_transition(self, state, char, stack):
        '''Пытается выполнить переход по текущему символу'''
        if not stack:
            return False, state
            
        stack_top = stack[-1]
        key = (state, char, stack_top)
        
        if key in self.transitions:
            new_state, stack_replacement = self.transitions[key]
            stack.pop()
            for symbol in reversed(stack_replacement):
                if symbol != 'ε':  # Игнорируем пустые символы
                    stack.append(symbol)
            return True, new_state
        return False, state

    def _try_epsilon_transition(self, state, stack):
        '''Пытается выполнить ε-переход'''
        if not stack:
            return False, state
            
        stack_top = stack[-1]
        key = (state, 'ε', stack_top)
        
        if key in self.transitions:
            new_state, stack_replacement = self.transitions[key]
            stack.pop()
            for symbol in reversed(stack_replacement):
                if symbol != 'ε':
                    stack.append(symbol)
            return True, new_state
        return False, state


def main():
    transitions = {
        ('q0', 'a', 'Z'): ('q1', 'aZ'),
        ('q0','b','Z'): ('q3','Z'),
        ('q0','b','a'): ('q2','a'),
        ('q1','a','a'): ('q0','aa'),
        ('q0','a','a'): ('q1','aa'),
        ('q1','b','a'): ('q2','a'),
        ('q2','b','a'): ('q2','a'),
        ('q2','c','a'): ('q3','ε'),
        ('q3','c','Z'): ('q4','ε'),
        ('q3','c','a'): ('q3','ε'),
    }
    
    dpda = DPDA(
        transitions=transitions,
        start_state='q0',
        start_stack='Z',
        final_states={'q4'}
    )
    
    test_cases = [
        "bc",  # +
        "aabccc",    # +
        "aacc",     # -
        "aaaabbbbbbccccc",     # +
        "aabbcc",     # -
        "ε", # -
    ]
    
    for test in test_cases:
        # Заменяем ε на пустую строку
        input_str = "" if test == "ε" else test
        accepted, reason = dpda.accepts(input_str)
        
        print(f"Цепочка '{test}': {reason}")
        print(f"Результат: {'Прошла' if accepted else 'Не прошла'}\n")


if __name__ == "__main__":
    main()