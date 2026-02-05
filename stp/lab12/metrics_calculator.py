import math
import ast
import inspect
from typing import Dict, List, Tuple, Any, Optional
import keyword
from collections import Counter


class CodeAnalyzer:
    """Анализатор кода для вычисления метрик Холстеда"""
    
    def __init__(self, source_code: str):
        """
        Инициализация анализатора с исходным кодом
        
        Args:
            source_code: исходный код функции
        """
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.operators = set()
        self.operands = set()
        self.operator_count = 0
        self.operand_count = 0
        
    def analyze(self) -> Dict[str, Any]:
        """Основной метод анализа кода"""
        self._traverse(self.tree)
        return self._calculate_metrics()
    
    def _traverse(self, node: ast.AST):
        """Рекурсивный обход AST"""
        # Обработка операторов
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Return, 
                           ast.Assign, ast.AugAssign, ast.AnnAssign,
                           ast.For, ast.While, ast.If, ast.With, ast.Try,
                           ast.ExceptHandler, ast.Assert, ast.Import, 
                           ast.ImportFrom, ast.Global, ast.Nonlocal,
                           ast.Expr, ast.Pass, ast.Break, ast.Continue,
                           ast.Raise, ast.Yield, ast.YieldFrom)):
            op_name = type(node).__name__
            self.operators.add(op_name)
            self.operator_count += 1
        
        # Обработка операций
        elif isinstance(node, (ast.UnaryOp, ast.BinOp, ast.BoolOp, 
                             ast.Compare, ast.Call, ast.Subscript,
                             ast.Attribute)):
            if isinstance(node, ast.UnaryOp):
                op = type(node.op).__name__
            elif isinstance(node, ast.BinOp):
                op = type(node.op).__name__
            elif isinstance(node, ast.BoolOp):
                op = type(node.op).__name__
            elif isinstance(node, ast.Compare):
                op = ','.join(type(op).__name__ for op in node.ops)
            else:
                op = type(node).__name__
            
            self.operators.add(op)
            self.operator_count += 1
        
        # Обработка операндов (идентификаторы и литералы)
        if isinstance(node, ast.Name):
            if node.id not in keyword.kwlist:
                self.operands.add(node.id)
                self.operand_count += 1
        
        elif isinstance(node, ast.Constant):
            value = str(node.value)
            self.operands.add(value)
            self.operand_count += 1
        
        # Обработка аргументов функции
        elif isinstance(node, ast.arg):
            self.operands.add(node.arg)
            self.operand_count += 1
        
        # Рекурсивный обход дочерних узлов
        for child in ast.iter_child_nodes(node):
            self._traverse(child)
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Вычисление всех метрик на основе собранных данных"""
        # Базовые метрики
        η1 = len(self.operators)  # число уникальных операторов
        η2 = len(self.operands)   # число уникальных операндов
        η = η1 + η2               # длина словаря
        
        N1 = self.operator_count  # общее число операторов
        N2 = self.operand_count   # общее число операндов
        N = N1 + N2               # длина реализации
        
        # Предсказанная длина по Холстеду
        if η1 > 0 and η2 > 0:
            N_hat = η1 * math.log2(η1) + η2 * math.log2(η2)
        else:
            N_hat = 0
        
        return {
            'η1': η1,
            'η2': η2,
            'η': η,
            'N1': N1,
            'N2': N2,
            'N': N,
            'N_hat': N_hat
        }


class AlgorithmMetricsCalculator:
    """Калькулятор метрических характеристик для алгоритмов"""
    
    def __init__(self):
        self.S = 18  # Константа Страуда (Stroud number)
    
    def calculate_all_metrics(self, function_source: str, η2_star: int) -> Dict[str, float]:
        """
        Вычисление всех метрических характеристик для функции
        
        Args:
            function_source: исходный код функции
            η2_star: число единых по смыслу входных и выходных параметров
        
        Returns:
            Словарь со всеми метриками
        """
        # Анализ кода
        analyzer = CodeAnalyzer(function_source)
        basic_metrics = analyzer.analyze()
        
        # Извлечение базовых метрик
        η1 = basic_metrics['η1']
        η2 = basic_metrics['η2']
        η = basic_metrics['η']
        N1 = basic_metrics['N1']
        N2 = basic_metrics['N2']
        N = basic_metrics['N']
        N_hat = basic_metrics['N_hat']
        
        # Потенциальный объем реализации
        if η2_star > 0:
            V_star = (2 + η2_star) * math.log2(2 + η2_star)
        else:
            V_star = 0
        
        # Объем реализации
        if η > 0:
            V = N * math.log2(η)
        else:
            V = 0
        
        # Уровень программы через потенциальный объем
        if V > 0:
            L = V_star / V
        else:
            L = 0
        
        # Уровень программы по реализации
        if η1 > 0 and N2 > 0:
            L_hat = (2 / η1) * (η2 / N2)
        else:
            L_hat = 0
        
        # Интеллектуальное содержание программы
        I = L_hat * V
        
        # Прогнозируемое время написания программы
        
        # T1: через потенциальный объем
        T1_hat = V_star / (2 * self.S)
        
        # T2: через длину реализации по Холстеду
        if η2 > 0 and self.S > 0:
            numerator = η1 * N * (η1 * math.log2(η1) + η2 * math.log2(η2)) * math.log2(η)
            denominator = 2 * self.S * η2
            if denominator != 0:
                T2_hat = numerator / denominator
            else:
                T2_hat = 0
        else:
            T2_hat = 0
        
        # T3: через метрические характеристики реализации
        if η2 > 0 and self.S > 0:
            numerator = η1 * N * N * math.log2(η)
            denominator = 2 * self.S * η2
            if denominator != 0:
                T3_hat = numerator / denominator
            else:
                T3_hat = 0
        else:
            T3_hat = 0
        
        # Уровни языков программирования
        λ1 = (L_hat ** 2) * V
        if V_star > 0:
            λ2 = (2 * V) / V_star
        else:
            λ2 = 0
        
        return {
            'η2_star': η2_star,
            'η1': η1,
            'η2': η2,
            'η': η,
            'N1': N1,
            'N2': N2,
            'N': N,
            'N_hat': N_hat,
            'V_star': V_star,
            'V': V,
            'L': L,
            'L_hat': L_hat,
            'I': I,
            'T1_hat': T1_hat,
            'T2_hat': T2_hat,
            'T3_hat': T3_hat,
            'λ1': λ1,
            'λ2': λ2
        }
    
    def analyze_function(self, func) -> Dict[str, Any]:
        """
        Анализ функции и вычисление её метрик
        
        Args:
            func: функция для анализа
        
        Returns:
            Словарь с метриками и исходным кодом
        """
        # Получаем исходный код функции
        source_code = inspect.getsource(func)
        
        # Оцениваем η2_star (число уникальных параметров)
        signature = inspect.signature(func)
        params = list(signature.parameters.keys())
        
        # Для простоты считаем каждый параметр как единый по смыслу
        # В реальности нужно анализировать семантику параметров
        η2_star = len(params)
        
        # Вычисляем все метрики
        metrics = self.calculate_all_metrics(source_code, η2_star)
        
        return {
            'name': func.__name__,
            'source': source_code,
            'params': params,
            'metrics': metrics
        }


def print_metrics_table(analysis_results: List[Dict[str, Any]]):
    """
    Печать таблицы с метрическими характеристиками
    
    Args:
        analysis_results: результаты анализа функций
    """
    print("\n" + "="*150)
    print("МЕТРИЧЕСКИЕ ХАРАКТЕРИСТИКИ РЕАЛИЗАЦИЙ АЛГОРИТМОВ")
    print("="*150)
    
    headers = [
        "Алгоритм", "η2*", "η1", "η2", "η", "N1", "N2", "N", "N^",
        "V*", "V", "L", "L^", "I", "T1^", "T2^", "T3^", "λ1", "λ2"
    ]
    
    # Форматирование заголовков
    header_fmt = "{:<15} {:>6} {:>4} {:>4} {:>4} {:>4} {:>4} {:>4} {:>7} " \
                 "{:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7}"
    
    print(header_fmt.format(*headers))
    print("-"*150)
    
    # Данные
    data_fmt = "{:<15} {:>6.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>7.2f} " \
               "{:>7.2f} {:>7.2f} {:>7.4f} {:>7.4f} {:>7.2f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f}"
    
    for result in analysis_results:
        metrics = result['metrics']
        print(data_fmt.format(
            result['name'],
            metrics['η2_star'],
            metrics['η1'],
            metrics['η2'],
            metrics['η'],
            metrics['N1'],
            metrics['N2'],
            metrics['N'],
            metrics['N_hat'],
            metrics['V_star'],
            metrics['V'],
            metrics['L'],
            metrics['L_hat'],
            metrics['I'],
            metrics['T1_hat'],
            metrics['T2_hat'],
            metrics['T3_hat'],
            metrics['λ1'],
            metrics['λ2']
        ))
    
    print("-"*150)
    
    # Вычисление средних значений
    avg_λ1 = sum(r['metrics']['λ1'] for r in analysis_results) / len(analysis_results)
    avg_λ2 = sum(r['metrics']['λ2'] for r in analysis_results) / len(analysis_results)
    
    print(f"\nСредние значения уровней языков программирования:")
    print(f"  λ1 (среднее): {avg_λ1:.4f}")
    print(f"  λ2 (среднее): {avg_λ2:.4f}")


def print_detailed_analysis(analysis_results: List[Dict[str, Any]]):
    """
    Подробный анализ результатов
    
    Args:
        analysis_results: результаты анализа
    """
    print("\n" + "="*80)
    print("ПОДРОБНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("="*80)
    
    for result in analysis_results:
        print(f"\nАлгоритм: {result['name']}")
        print(f"Параметры: {result['params']}")
        print("-"*40)
        
        metrics = result['metrics']
        
        print(f"η2* (параметры): {metrics['η2_star']:.0f}")
        print(f"η1 (уникальные операторы): {metrics['η1']:.0f}")
        print(f"η2 (уникальные операнды): {metrics['η2']:.0f}")
        print(f"η (словарь): {metrics['η']:.0f}")
        print(f"N (длина реализации): {metrics['N']:.0f}")
        print(f"N^ (прогноз по Холстеду): {metrics['N_hat']:.2f}")
        
        # Анализ точности прогноза
        if metrics['N'] > 0:
            error_percent = abs(metrics['N'] - metrics['N_hat']) / metrics['N'] * 100
            print(f"Ошибка прогноза длины: {error_percent:.2f}%")
        
        print(f"V (объем): {metrics['V']:.2f}")
        print(f"V* (потенциальный объем): {metrics['V_star']:.2f}")
        print(f"L (уровень): {metrics['L']:.4f}")
        print(f"L^ (уровень по реализации): {metrics['L_hat']:.4f}")
        print(f"I (интеллектуальное содержание): {metrics['I']:.2f}")
        print(f"T1^ (время через V*): {metrics['T1_hat']:.4f} сек")
        print(f"T2^ (время через N^): {metrics['T2_hat']:.4f} сек")
        print(f"T3^ (время через N): {metrics['T3_hat']:.4f} сек")
        print(f"λ1: {metrics['λ1']:.4f}")
        print(f"λ2: {metrics['λ2']:.4f}")


def main():
    """Основная функция анализа метрик"""
    from algorithms import (
        find_min_1d, bubble_sort, binary_search, 
        find_min_2d, reverse_array, cyclic_shift_left, replace_all
    )
    
    print("ЛАБОРАТОРНАЯ РАБОТА №2")
    print("Вычисление метрических характеристик реализаций алгоритмов")
    print("="*60)
    
    # Создаем калькулятор метрик
    calculator = AlgorithmMetricsCalculator()
    
    # Анализируем все алгоритмы
    functions = [
        find_min_1d,      # 1. Поиск минимума в 1D массиве
        bubble_sort,      # 2. Сортировка пузырьком
        binary_search,    # 3. Бинарный поиск
        find_min_2d,      # 4. Поиск минимума в 2D массиве
        reverse_array,    # 5. Разворот массива
        cyclic_shift_left, # 6. Циклический сдвиг
        replace_all       # 7. Замена всех вхождений
    ]
    
    # Собираем результаты анализа
    results = []
    for func in functions:
        print(f"Анализ алгоритма: {func.__name__}...")
        result = calculator.analyze_function(func)
        results.append(result)
    
    # Выводим таблицу с метриками
    print_metrics_table(results)
    
    # Подробный анализ
    print_detailed_analysis(results)
    
    # Сводный анализ
    print("\n" + "="*80)
    print("СВОДНЫЙ АНАЛИЗ ПО ВСЕМ АЛГОРИТМАМ")
    print("="*80)
    
    # Группировка по сложности
    print("\nГруппировка алгоритмов по объему реализации (V):")
    for result in sorted(results, key=lambda x: x['metrics']['V']):
        print(f"  {result['name']:20} V = {result['metrics']['V']:7.2f}")
    
    # Средние значения
    avg_N = sum(r['metrics']['N'] for r in results) / len(results)
    avg_V = sum(r['metrics']['V'] for r in results) / len(results)
    avg_L = sum(r['metrics']['L'] for r in results) / len(results)
    
    print(f"\nСредние значения по всем алгоритмам:")
    print(f"  Средняя длина реализации (N): {avg_N:.2f}")
    print(f"  Средний объем (V): {avg_V:.2f}")
    print(f"  Средний уровень программы (L): {avg_L:.4f}")
    
    # Анализ точности прогноза длины
    print("\nАнализ точности прогноза длины реализации (N^ vs N):")
    total_error = 0
    for result in results:
        N = result['metrics']['N']
        N_hat = result['metrics']['N_hat']
        error = abs(N - N_hat) / N * 100 if N > 0 else 0
        total_error += error
        print(f"  {result['name']:20} N={N:4.0f}, N^={N_hat:6.2f}, ошибка={error:6.2f}%")
    
    avg_error = total_error / len(results)
    print(f"\n  Средняя ошибка прогноза: {avg_error:.2f}%")
    
    print("\n" + "="*80)
    print("ВЫВОДЫ:")
    print("="*80)
    print("1. Метрики Холстеда позволяют количественно оценить сложность алгоритмов.")
    print("2. Объем реализации (V) коррелирует с субъективной сложностью алгоритма.")
    print("3. Прогноз длины реализации (N^) имеет ошибку около 10-30%.")
    print("4. Уровень программы (L) показывает качество реализации.")
    print("5. Интеллектуальное содержание (I) отражает сложность задачи.")
    print("6. Метрики позволяют сравнивать разные реализации одних и тех же алгоритмов.")


if __name__ == "__main__":
    main()