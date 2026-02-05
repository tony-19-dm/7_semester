import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from tkinter import ttk

class InputValidator:
    def __init__(self, alphabet_var, symbol_var, count_var, substring_var, min_len_var, max_len_var):
        self.alphabet_var = alphabet_var
        self.symbol_var = symbol_var
        self.count_var = count_var
        self.substring_var = substring_var
        self.min_len_var = min_len_var
        self.max_len_var = max_len_var
    
    def calculate_min_possible_length(self):
        """Вычисление минимальной возможной длины цепочки"""
        symbol = self.symbol_var.get().strip()
        count = self.count_var.get()
        substring = self.substring_var.get().strip()
        
        # Количество нужного символа в подцепочке
        symbol_in_substring = substring.count(symbol)
        
        # Если в подцепочке уже достаточно символов
        if symbol_in_substring >= count:
            return len(substring)
        else:
            # Нужно добавить недостающие символы
            additional_symbols_needed = count - symbol_in_substring
            return len(substring) + additional_symbols_needed
    
    def validate(self):
        """Проверка корректности введенных данных"""
        try:
            # Проверка алфавита
            alphabet = self.alphabet_var.get().strip().split()
            if not alphabet:
                raise ValueError("Алфавит не может быть пустым")
            if len(alphabet) > 10:
                raise ValueError("Алфавит слишком большой (макс. 10 символов)")
            if len(alphabet) != len(set(alphabet)):
                raise ValueError("Алфавит не должен содержать повторяющихся символов")
            
            # Проверка символа для подсчета
            symbol = self.symbol_var.get().strip()
            if not symbol:
                raise ValueError("Символ для подсчета не указан")
            if symbol not in alphabet:
                raise ValueError("Символ для подсчета должен принадлежать алфавиту")
            
            # Проверка кратности
            count = self.count_var.get()
            if count < 0:
                raise ValueError("Кратность должна быть неотрицательной")
            
            # Проверка подцепочки
            substring = self.substring_var.get().strip()
            if not substring:
                raise ValueError("Подцепочка не может быть пустой")
            for ch in substring:
                if ch not in alphabet:
                    raise ValueError(f"Символ '{ch}' из подцепочки отсутствует в алфавите")
            
            # Проверка минимальной возможной длины
            min_possible_length = self.calculate_min_possible_length()
            
            # Проверка длин
            min_len = self.min_len_var.get()
            max_len = self.max_len_var.get()
            
            if min_len > max_len:
                raise ValueError("Минимальная длина не может превышать максимальную")
            
            if min_len < min_possible_length:
                raise ValueError(f"Минимальная длина ({min_len}) меньше минимально возможной ({min_possible_length})")
            
            # Проверка максимальной длины
            if max_len > 15:
                if not messagebox.askyesno("Предупреждение", 
                                          f"Максимальная длина {max_len} может привести к генерации очень большого числа цепочек.\n"
                                          f"Это может замедлить работу программы.\n"
                                          f"Продолжить?"):
                    return False
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return False

def show_steps_dialog(parent, chains, generation_steps, steps_text_widget, 
                     substring_var, symbol_var, count_var, grammar_type_var):
    """Диалог для показа шагов генерации"""
    dialog = tk.Toplevel(parent)
    dialog.title("Выбор цепочки для просмотра шагов")
    dialog.geometry("500x400")
    
    tk.Label(dialog, text="Выберите цепочку:").pack(pady=10)
    
    listbox = tk.Listbox(dialog, selectmode=tk.SINGLE, height=15)
    scrollbar = tk.Scrollbar(dialog)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    for chain in chains:
        listbox.insert(tk.END, f"{chain} (длина: {len(chain)})")
    
    def show_steps():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите цепочку!")
            return
        
        idx = selection[0]
        steps = generation_steps[idx]
        
        # Показать шаги в основном окне
        steps_text_widget.delete(1.0, tk.END)
        
        # Заголовок
        steps_text_widget.insert(tk.END, f"ДЕТАЛЬНЫЙ ВЫВОД ЦЕПОЧКИ: {chains[idx]}\n")
        steps_text_widget.insert(tk.END, f"Тип грамматики: {grammar_type_var.get()}\n")
        steps_text_widget.insert(tk.END, "="*60 + "\n\n")
        
        # Вывод шагов с правилами
        for i, (rule, description) in enumerate(steps, 1):
            steps_text_widget.insert(tk.END, f"Шаг {i}:\n")
            steps_text_widget.insert(tk.END, f"  Правило: {rule}\n")
            steps_text_widget.insert(tk.END, f"  Действие: {description}\n")
            
            # Добавляем разделитель между шагами
            if i < len(steps):
                steps_text_widget.insert(tk.END, "  " + "-"*40 + "\n")
        
        # Добавляем информацию о проверке
        steps_text_widget.insert(tk.END, "\n" + "="*60 + "\n")
        steps_text_widget.insert(tk.END, "ПРОВЕРКА УСЛОВИЙ:\n")
        steps_text_widget.insert(tk.END, f"1. Цепочка заканчивается на '{substring_var.get()}': ДА\n")
        
        symbol_count = chains[idx].count(symbol_var.get())
        required_count = count_var.get()
        steps_text_widget.insert(tk.END, f"2. Символ '{symbol_var.get()}' встречается {symbol_count} раз: ")
        if symbol_count == required_count:
            steps_text_widget.insert(tk.END, f"ДА (требуется {required_count})\n")
        else:
            steps_text_widget.insert(tk.END, f"НЕТ (требуется {required_count})\n")
        
        dialog.destroy()
        
        # Переключиться на вкладку с шагами
        notebook = parent.winfo_children()[0]
        notebook.select(2)  # Третья вкладка
    
    tk.Button(dialog, text="Показать шаги вывода", command=show_steps).pack(pady=10)

def save_to_file(grammar, chains, generation_steps, params, calculate_min_length):
    """Сохранение результатов в файл"""
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Сохранить результаты"
    )
    
    if not filename:
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ РЕГУЛЯРНОЙ ГРАММАТИКИ\n")
        f.write("="*60 + "\n\n")
        
        # Параметры
        f.write("ПАРАМЕТРЫ ЯЗЫКА:\n")
        f.write(f"Алфавит: {params['alphabet']}\n")
        f.write(f"Символ для подсчета: {params['symbol']}\n")
        f.write(f"Кратность: {params['count']}\n")
        f.write(f"Подцепочка: {params['substring']}\n")
        f.write(f"Тип грамматики: {params['grammar_type']}\n")
        f.write(f"Диапазон длин: {params['min_len']} - {params['max_len']}\n")
        min_possible_length = calculate_min_length()
        f.write(f"Минимальная возможная длина: {min_possible_length}\n\n")
        
        # Грамматика
        f.write("ПОСТРОЕННАЯ ГРАММАТИКА:\n")
        f.write(f"Тип: {grammar.get('type', 'N/A')}\n")
        f.write("Правила:\n")
        for rule in grammar.get("rules", []):
            f.write(f"  {rule}\n")
        f.write("\n")
        
        # Цепочки
        if chains:
            f.write("СГЕНЕРИРОВАННЫЕ ЦЕПОЧКИ:\n")
            f.write(f"Всего: {len(chains)}\n\n")
            for i, chain in enumerate(chains, 1):
                f.write(f"{i:3}. {chain} (длина: {len(chain)})\n")
            
            # Статистика
            if chains:
                lengths = [len(chain) for chain in chains]
                f.write(f"\nСТАТИСТИКА:\n")
                f.write(f"Минимальная длина: {min(lengths)}\n")
                f.write(f"Максимальная длина: {max(lengths)}\n")
                f.write(f"Средняя длина: {sum(lengths)/len(lengths):.2f}\n")
                
            # Пример шагов вывода для первой цепочки
            if chains and generation_steps:
                f.write("\n" + "="*60 + "\n")
                f.write("ПРИМЕР ВЫВОДА ЦЕПОЧКИ:\n")
                f.write(f"Цепочка: {chains[0]}\n")
                f.write("Шаги вывода:\n")
                for i, (rule, description) in enumerate(generation_steps[0], 1):
                    f.write(f"  Шаг {i}: {rule} - {description}\n")
        else:
            f.write("Цепочки не сгенерированы или не найдены.\n")
    
    messagebox.showinfo("Успех", f"Результаты сохранены в файл:\n{filename}")

def show_help_dialog(parent):
    """Показать диалог справки"""
    help_text = """
ФОРМАТ ВВОДА ДАННЫХ:

1. Алфавит: символы через пробел
   Пример: a b c
   Ограничения: максимум 10 символов, без повторений

2. Символ для подсчета: один символ из алфавита
   Пример: a

3. Кратность вхождения: целое число ≥ 0
   Пример: 2 (символ 'a' должен встречаться ровно 2 раза)

4. Обязательная подцепочка: строка из символов алфавита
   Пример: bc (все цепочки должны заканчиваться на 'bc')

5. Тип грамматики:
   - LL (леворекурсивная, леволинейная)
   - PL (праворекурсивная, праволинейная)

6. Диапазон длин: минимальная и максимальная длина цепочек
   Минимальная длина автоматически ограничивается минимально возможной

ОТОБРАЖЕНИЕ ШАГОВ ГЕНЕРАЦИИ:

При просмотре шагов генерации для каждой цепочки программа показывает:
1. Какое правило грамматики применяется на каждом шаге
2. Описание действия (какой символ добавляется и в какое состояние переходим)
3. Проверку всех условий для цепочки

ПРИМЕР ДЛЯ ГРАММАТИКИ LL:
   Алфавит: a b c
   Символ: a
   Кратность: 2
   Подцепочка: bc
   Диапазон: 4-6

   Пример цепочки: aabc
   Шаги вывода:
     Шаг 1: S → A0
     Шаг 2: A0 → a A1  (добавляем 'a', переходим в состояние A1)
     Шаг 3: A1 → a A2  (добавляем 'a', переходим в состояние A2)
     Шаг 4: A2 → b B1  (начинаем подцепочку: добавляем 'b')
     Шаг 5: B1 → c B2  (продолжаем подцепочку: добавляем 'c')
     Шаг 6: B2 → ε     (завершаем подцепочку)
     Результат: aabc

ОГРАНИЧЕНИЯ:
- Максимальная длина цепочки: 15 символов (для производительности)
- Максимальный размер алфавита: 10 символов
- Программа предупредит, если генерация может создать слишком много комбинаций
    """
    
    help_window = tk.Toplevel(parent)
    help_window.title("Справка")
    help_window.geometry("600x500")
    
    text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_widget.insert(tk.END, help_text)
    text_widget.config(state=tk.DISABLED)

def show_info_dialog(title, message):
    """Показать информационное сообщение"""
    messagebox.showinfo(title, message)