import tkinter.messagebox as messagebox
from itertools import product
from grammar_generator import GrammarGenerator

class ChainGenerator:
    def __init__(self):
        self.grammar_generator = GrammarGenerator()
    
    def generate_chains(self, alphabet, symbol, count, substring, min_len, max_len, grammar_type):
        """Генерация всех цепочек в заданном диапазоне длин"""
        chains = []
        generation_steps = []
        
        # Проверка минимальной возможной длины
        min_possible_length = self.grammar_generator.calculate_min_possible_length(substring, symbol, count)
        if min_len < min_possible_length:
            raise ValueError(f"Минимальная длина ({min_len}) меньше минимально возможной ({min_possible_length})")
        
        # Количество символов symbol в подцепочке
        symbol_in_substring = substring.count(symbol)
        
        # Сколько символов symbol нужно добавить в префикс
        needed_in_prefix = max(0, count - symbol_in_substring)
        
        # Длина префикса (без учета подцепочки)
        min_prefix_len = max(needed_in_prefix, min_len - len(substring))
        max_prefix_len = max_len - len(substring)
        
        if max_prefix_len < 0:
            return {"chains": [], "generation_steps": []}
        
        # Ограничение по производительности
        estimated_combinations = sum(len(alphabet)**i for i in range(min_prefix_len, max_prefix_len + 1))
        if estimated_combinations > 100000:
            if not messagebox.askyesno("Предупреждение", 
                                      f"Генерация может создать более {estimated_combinations:,} комбинаций.\n"
                                      f"Это может занять много времени и памяти.\n"
                                      f"Продолжить?"):
                return {"chains": [], "generation_steps": []}
        
        # Генерация цепочек с учетом кратности символа
        generated_count = 0
        
        for prefix_len in range(min_prefix_len, max_prefix_len + 1):
            # Все комбинации символов алфавита заданной длины
            for combination in product(alphabet, repeat=prefix_len):
                chain = ''.join(combination) + substring
                
                # Проверка кратности символа в префиксе
                prefix = ''.join(combination)
                if prefix.count(symbol) != needed_in_prefix:
                    continue  # В префиксе должно быть ровно needed_in_prefix символов symbol
                
                # Проверка кратности символа во всей цепочке
                if chain.count(symbol) == count:
                    # Проверка длины
                    if min_len <= len(chain) <= max_len:
                        chains.append(chain)
                        generated_count += 1
                        
                        # Генерация шагов вывода
                        derivation_steps = self.grammar_generator.generate_derivation_steps(
                            chain, alphabet, symbol, count, substring, grammar_type
                        )
                        generation_steps.append(derivation_steps)
                
                if generated_count > 10000:
                    if not messagebox.askyesno("Предупреждение", 
                                              f"Сгенерировано уже {generated_count} цепочек.\n"
                                              f"Продолжить генерацию?"):
                        break
            if generated_count > 10000:
                break
        
        # Сортировка цепочек по длине и лексикографии
        chains.sort(key=lambda x: (len(x), x))
        
        return {
            "chains": chains,
            "generation_steps": generation_steps
        }