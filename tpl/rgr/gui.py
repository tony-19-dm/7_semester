import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from grammar_generator import GrammarGenerator
from chain_generator import ChainGenerator
from utils import show_info_dialog

class RegularGrammarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор регулярных грамматик")
        self.root.geometry("900x700")
        
        # Инициализация компонентов
        self.grammar_generator = GrammarGenerator()
        self.chain_generator = ChainGenerator()
        
        # Переменные для данных
        self.alphabet_var = tk.StringVar()
        self.symbol_var = tk.StringVar()
        self.count_var = tk.IntVar(value=1)
        self.substring_var = tk.StringVar()
        self.grammar_type_var = tk.StringVar(value="LL")
        self.min_len_var = tk.IntVar(value=1)
        self.max_len_var = tk.IntVar(value=5)
        
        # Результаты
        self.grammar = {}
        self.chains = []
        self.generation_steps = []
        
        self.create_menu()
        self.create_widgets()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить результаты", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню "Информация"
        info_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Информация", menu=info_menu)
        info_menu.add_command(label="Автор", command=self.show_author)
        info_menu.add_command(label="Тема", command=self.show_topic)
        info_menu.add_command(label="Справка", command=self.show_help)
        
        # Меню "Расчеты"
        calc_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Расчеты", menu=calc_menu)
        calc_menu.add_command(label="Построить грамматику", command=self.build_grammar)
        calc_menu.add_command(label="Сгенерировать цепочки", command=self.generate_chains)
        calc_menu.add_command(label="Показать шаги генерации", command=self.show_generation_steps)
    
    def create_widgets(self):
        # Основной фрейм с вкладками
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка ввода данных
        self.create_input_tab(notebook)
        
        # Вкладка результатов
        self.create_results_tab(notebook)
        
        # Вкладка шагов генерации
        self.create_steps_tab(notebook)
    
    def create_input_tab(self, notebook):
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text="Ввод данных")
        
        ttk.Label(input_frame, text="Алфавит (символы через пробел):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Entry(input_frame, textvariable=self.alphabet_var, width=40).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Символ для подсчета кратности:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Entry(input_frame, textvariable=self.symbol_var, width=40).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Кратность вхождения:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Spinbox(input_frame, from_=0, to=20, textvariable=self.count_var, width=38).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Обязательная подцепочка в конце:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Entry(input_frame, textvariable=self.substring_var, width=40).grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Тип грамматики:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        grammar_combo = ttk.Combobox(input_frame, textvariable=self.grammar_type_var, 
                                   values=["LL", "PL"], state="readonly", width=37)
        grammar_combo.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Минимальная длина цепочки:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Spinbox(input_frame, from_=1, to=20, textvariable=self.min_len_var, width=38).grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Максимальная длина цепочки:").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Spinbox(input_frame, from_=1, to=20, textvariable=self.max_len_var, width=38).grid(row=6, column=1, padx=10, pady=5)
        
        # Кнопки управления
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Построить грамматику", command=self.build_grammar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сгенерировать цепочки", command=self.generate_chains).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_all).pack(side=tk.LEFT, padx=5)
    
    def create_results_tab(self, notebook):
        result_frame = ttk.Frame(notebook)
        notebook.add(result_frame, text="Результаты")
        
        # Грамматика
        ttk.Label(result_frame, text="Построенная грамматика:").pack(anchor=tk.W, padx=10, pady=(10,0))
        self.grammar_text = scrolledtext.ScrolledText(result_frame, height=10, width=80)
        self.grammar_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Цепочки
        ttk.Label(result_frame, text="Сгенерированные цепочки:").pack(anchor=tk.W, padx=10, pady=(10,0))
        self.chains_text = scrolledtext.ScrolledText(result_frame, height=15, width=80)
        self.chains_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    def create_steps_tab(self, notebook):
        steps_frame = ttk.Frame(notebook)
        notebook.add(steps_frame, text="Шаги генерации")
        
        self.steps_text = scrolledtext.ScrolledText(steps_frame, height=25, width=80)
        self.steps_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def validate_input(self):
        """Проверка корректности введенных данных"""
        from utils import InputValidator
        validator = InputValidator(
            alphabet_var=self.alphabet_var,
            symbol_var=self.symbol_var,
            count_var=self.count_var,
            substring_var=self.substring_var,
            min_len_var=self.min_len_var,
            max_len_var=self.max_len_var
        )
        return validator.validate()
    
    def build_grammar(self):
        """Построение регулярной грамматики"""
        if not self.validate_input():
            return
        
        try:
            alphabet = self.alphabet_var.get().strip().split()
            symbol = self.symbol_var.get().strip()
            count = self.count_var.get()
            substring = self.substring_var.get().strip()
            grammar_type = self.grammar_type_var.get()
            
            # Используем GrammarGenerator для построения грамматики
            self.grammar = self.grammar_generator.build_grammar(
                alphabet, symbol, count, substring, grammar_type
            )
            
            # Вывод грамматики
            self.grammar_text.delete(1.0, tk.END)
            self.grammar_text.insert(tk.END, f"Тип грамматики: {grammar_type}\n")
            self.grammar_text.insert(tk.END, f"Алфавит: {' '.join(alphabet)}\n")
            self.grammar_text.insert(tk.END, f"Символ для подсчета: {symbol} (кратность: {count})\n")
            self.grammar_text.insert(tk.END, f"Подцепочка: {substring}\n")
            
            min_possible_length = self.grammar_generator.calculate_min_possible_length(substring, symbol, count)
            self.grammar_text.insert(tk.END, f"Минимальная возможная длина: {min_possible_length}\n")
            
            self.grammar_text.insert(tk.END, "\nПравила грамматики:\n")
            for rule in self.grammar["rules"]:
                self.grammar_text.insert(tk.END, f"  {rule}\n")
            
            messagebox.showinfo("Успех", "Грамматика успешно построена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении грамматики: {str(e)}")
    
    def generate_chains(self):
        """Генерация всех цепочек в заданном диапазоне длин"""
        if not self.grammar:
            messagebox.showwarning("Предупреждение", "Сначала постройте грамматику!")
            return
        
        if not self.validate_input():
            return
        
        try:
            alphabet = self.alphabet_var.get().strip().split()
            symbol = self.symbol_var.get().strip()
            count = self.count_var.get()
            substring = self.substring_var.get().strip()
            min_len = self.min_len_var.get()
            max_len = self.max_len_var.get()
            grammar_type = self.grammar_type_var.get()
            
            # Используем ChainGenerator для генерации цепочек
            result = self.chain_generator.generate_chains(
                alphabet=alphabet,
                symbol=symbol,
                count=count,
                substring=substring,
                min_len=min_len,
                max_len=max_len,
                grammar_type=grammar_type
            )
            
            self.chains = result["chains"]
            self.generation_steps = result["generation_steps"]
            
            # Вывод результатов
            self.chains_text.delete(1.0, tk.END)
            if self.chains:
                self.chains_text.insert(tk.END, f"Найдено цепочек: {len(self.chains)}\n\n")
                for i, chain in enumerate(self.chains, 1):
                    self.chains_text.insert(tk.END, f"{i:3}. {chain} (длина: {len(chain)})\n")
                
                # Вывод статистики
                self.chains_text.insert(tk.END, f"\nСтатистика:\n")
                lengths = [len(chain) for chain in self.chains]
                self.chains_text.insert(tk.END, f"Минимальная длина: {min(lengths)}\n")
                self.chains_text.insert(tk.END, f"Максимальная длина: {max(lengths)}\n")
                self.chains_text.insert(tk.END, f"Средняя длина: {sum(lengths)/len(lengths):.2f}\n")
                
                # Вывод примера минимальной цепочки
                min_chain = min(self.chains, key=len)
                self.chains_text.insert(tk.END, f"\nПример минимальной цепочки: {min_chain}\n")
            else:
                min_possible_length = self.grammar_generator.calculate_min_possible_length(substring, symbol, count)
                self.chains_text.insert(tk.END, "Цепочки не найдены в заданном диапазоне.\n")
                self.chains_text.insert(tk.END, "Возможные причины:\n")
                self.chains_text.insert(tk.END, "1. Заданная кратность не достигается\n")
                self.chains_text.insert(tk.END, "2. Диапазон длин слишком мал\n")
                self.chains_text.insert(tk.END, f"3. Минимальная возможная длина: {min_possible_length}\n")
                self.chains_text.insert(tk.END, "4. Неправильные параметры языка\n")
            
            # Очистка шагов генерации
            self.steps_text.delete(1.0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации цепочек: {str(e)}")
    
    def show_generation_steps(self):
        """Показать шаги генерации для выбранной цепочки"""
        from utils import show_steps_dialog
        
        if not self.chains:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте цепочки!")
            return
        
        show_steps_dialog(
            parent=self.root,
            chains=self.chains,
            generation_steps=self.generation_steps,
            steps_text_widget=self.steps_text,
            substring_var=self.substring_var,
            symbol_var=self.symbol_var,
            count_var=self.count_var,
            grammar_type_var=self.grammar_type_var
        )
    
    def save_results(self):
        """Сохранение результатов в файл"""
        from utils import save_to_file
        
        if not self.grammar:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения!")
            return
        
        try:
            params = {
                'alphabet': self.alphabet_var.get(),
                'symbol': self.symbol_var.get(),
                'count': self.count_var.get(),
                'substring': self.substring_var.get(),
                'grammar_type': self.grammar_type_var.get(),
                'min_len': self.min_len_var.get(),
                'max_len': self.max_len_var.get()
            }
            
            save_to_file(
                grammar=self.grammar,
                chains=self.chains,
                generation_steps=self.generation_steps,
                params=params,
                calculate_min_length=lambda: self.grammar_generator.calculate_min_possible_length(
                    params['substring'], params['symbol'], params['count']
                )
            )
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
    
    def show_author(self):
        """Информация об авторе"""
        messagebox.showinfo("Автор", 
            "Разработчик: Дмитриев Антон\n"
            "Группа: ИП-213\n")
    
    def show_topic(self):
        """Информация о теме задания"""
        messagebox.showinfo("Тема задания",
            "ПОСТРОЕНИЕ РЕГУЛЯРНОЙ ГРАММАТИКИ\n\n"
            "Задание:\n"
            "Разработать программу, которая по предложенному описанию языка\n"
            "построит регулярную грамматику (ЛЛ или ПЛ – по выбору пользователя),\n"
            "задающую этот язык, и позволит сгенерировать с её помощью все цепочки\n"
            "языка в заданном диапазоне длин.\n\n"
            "Параметры языка:\n"
            "1. Алфавит\n"
            "2. Кратность вхождения некоторого символа алфавита\n"
            "3. Обязательная фиксированная подцепочка, на которую заканчиваются\n"
            "   все цепочки языка")
    
    def show_help(self):
        """Справка с примером формата данных"""
        from utils import show_help_dialog
        show_help_dialog(self.root)
    
    def clear_all(self):
        """Очистка всех полей"""
        self.grammar_text.delete(1.0, tk.END)
        self.chains_text.delete(1.0, tk.END)
        self.steps_text.delete(1.0, tk.END)
        self.grammar = {}
        self.chains = []
        self.generation_steps = []