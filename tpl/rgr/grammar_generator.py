class GrammarGenerator:
    def __init__(self):
        pass
    
    def calculate_min_possible_length(self, substring, symbol, count):
        """Вычисление минимальной возможной длины цепочки"""
        symbol_in_substring = substring.count(symbol)
        
        if symbol_in_substring >= count:
            return len(substring)
        else:
            additional_symbols_needed = count - symbol_in_substring
            return len(substring) + additional_symbols_needed
    
    def _effective_count_needed(self, substring, symbol, count):
        """Вычисляет, сколько символов нужно добавить в префикс"""
        symbol_in_substring = substring.count(symbol)
        return max(0, count - symbol_in_substring)
    
    def build_grammar(self, alphabet, symbol, count, substring, grammar_type):
        """Построение регулярной грамматики"""
        grammar = {}
        
        symbol_in_substring = substring.count(symbol)
        
        needed_in_prefix = self._effective_count_needed(substring, symbol, count)
        
        if grammar_type == "LL":  # Левосторонняя грамматика
            rules = []
            
            # Начальное правило
            rules.append("S -> A0")

            # Правила для префикса (нужно набрать needed_in_prefix символов symbol)
            for k in range(needed_in_prefix + 1):
                for a in alphabet:
                    if a == symbol and k < needed_in_prefix:
                        rules.append(f"A{k} -> {a} A{k+1}")
                    elif a != symbol:
                        rules.append(f"A{k} -> {a} A{k}")
            
            # Правила для подцепочки
            if len(substring) > 0:
                # Первый символ подцепочки
                rules.append(f"A{needed_in_prefix} -> {substring[0]} B1")
                
                # Остальные символы подцепочки
                for i in range(1, len(substring)):
                    rules.append(f"B{i} -> {substring[i]} B{i+1}")
                
                # Завершение
                rules.append(f"B{len(substring)} -> ε")
            else:
                # Если подцепочка пустая (хотя по условию не должна быть)
                rules.append(f"A{needed_in_prefix} -> ε")
            
            grammar = {"type": "LL", "rules": rules, "needed_in_prefix": needed_in_prefix}
            
        else:  # Правосторонняя грамматика
            rules = []
            
            rules.append("S -> A0")

            # Правила для префикса
            for k in range(needed_in_prefix + 1):
                for a in alphabet:
                    if a == symbol and k < needed_in_prefix:
                        rules.append(f"A{k} -> A{k+1} {a}")
                    elif a != symbol:
                        rules.append(f"A{k} -> A{k} {a}")
            
            # Правила для подцепочки
            if len(substring) > 0:
                # Переход к генерации подцепочки
                rules.append(f"A{needed_in_prefix} -> A_sub {substring[0]}")
                
                # Генерация остальной части подцепочки
                for i in range(1, len(substring)):
                    rules.append(f"A_sub -> A_sub {substring[i]}")
                
                rules.append("A_sub -> ε")
            else:
                rules.append(f"A{needed_in_prefix} -> ε")
            
            grammar = {"type": "PL", "rules": rules, "needed_in_prefix": needed_in_prefix}
        
        return grammar
    
    def generate_derivation_steps(self, chain, alphabet, symbol, count, substring, grammar_type):
        """Генерация шагов вывода для цепочки с отображением правил"""
        steps = []
        
        # Количество символов symbol в подцепочке
        symbol_in_substring = substring.count(symbol)
        
        # Сколько символов symbol нужно добавить в префикс
        needed_in_prefix = self._effective_count_needed(substring, symbol, count)
        
        if grammar_type == "LL":
            # Для леволинейной грамматики
            if chain.endswith(substring):
                prefix = chain[:-len(substring)]
            else:
                prefix = chain
            
            # Шаг 1: Начальный символ
            steps.append(("S", "Начальный символ"))
            
            # Шаг 2: Применяем S -> A0
            steps.append(("S → A0", "Применяем начальное правило"))
            
            current_state = 0
            current_symbol_count = 0  # Счетчик символов symbol в префиксе
            
            # Генерация префикса
            for i, ch in enumerate(prefix):
                if ch == symbol and current_symbol_count < needed_in_prefix:
                    # Применяем правило A{k} -> a A{k+1}
                    rule = f"A{current_state} → {ch} A{current_state+1}"
                    current_state += 1
                    current_symbol_count += 1
                    steps.append((rule, f"Добавляем '{ch}', переходим в состояние A{current_state}"))
                else:
                    # Применяем правило A{k} -> a A{k}
                    rule = f"A{current_state} → {ch} A{current_state}"
                    steps.append((rule, f"Добавляем '{ch}', остаемся в состоянии A{current_state}"))
            
            # Проверяем, что достигли нужного состояния
            if current_state != needed_in_prefix:
                # Если не достигли нужного состояния, значит цепочка некорректна
                steps.append(("ОШИБКА", f"Не достигнуто состояние A{needed_in_prefix}"))
                return steps
            
            # Генерация подцепочки
            if len(substring) > 0:
                # Первый символ подцепочки
                rule = f"A{current_state} → {substring[0]} B1"
                steps.append((rule, f"Начинаем подцепочку: добавляем '{substring[0]}'"))
                
                # Остальные символы подцепочки
                for i in range(1, len(substring)):
                    rule = f"B{i} → {substring[i]} B{i+1}"
                    steps.append((rule, f"Продолжаем подцепочку: добавляем '{substring[i]}'"))
                
                # Завершение
                rule = f"B{len(substring)} → ε"
                steps.append((rule, "Завершаем подцепочку"))
            
            # Финальный шаг
            steps.append((f"Результат: {chain}", "Цепочка успешно построена"))
            
        else:  # PL - праворекурсивная грамматика
            # Для праворекурсивной грамматики
            if chain.endswith(substring):
                prefix = chain[:-len(substring)]
            else:
                prefix = chain
            
            # Шаг 1: Начальный символ
            steps.append(("S", "Начальный символ"))
            
            # Шаг 2: Применяем S -> A0
            steps.append(("S → A0", "Применяем начальное правило"))
            
            current_state = 0
            current_symbol_count = 0  # Счетчик символов symbol в префиксе
            
            # Генерация префикса (в обратном порядке для PL)
            for ch in prefix:
                if ch == symbol and current_symbol_count < needed_in_prefix:
                    rule = f"A{current_state} → A{current_state+1} {ch}"
                    current_state += 1
                    current_symbol_count += 1
                    steps.append((rule, f"Добавляем '{ch}' справа, переходим в A{current_state}"))
                else:
                    rule = f"A{current_state} → A{current_state} {ch}"
                    steps.append((rule, f"Добавляем '{ch}' справа, остаемся в A{current_state}"))
            
            # Проверяем, что достигли нужного состояния
            if current_state != needed_in_prefix:
                steps.append(("ОШИБКА", f"Не достигнуто состояние A{needed_in_prefix}"))
                return steps
            
            # Генерация подцепочки
            if len(substring) > 0:
                # Переход к подцепочке
                rule = f"A{current_state} → A_sub {substring[0]}"
                steps.append((rule, f"Начинаем подцепочку: добавляем '{substring[0]}' справа"))
                
                # Генерация остальной части подцепочки
                for i in range(1, len(substring)):
                    rule = f"A_sub → A_sub {substring[i]}"
                    steps.append((rule, f"Продолжаем подцепочку: добавляем '{substring[i]}' справа"))
                
                # Завершение
                steps.append(("A_sub → ε", "Завершаем подцепочку"))
            
            # Финальный шаг
            steps.append((f"Результат: {chain}", "Цепочка успешно построена"))
        
        return steps