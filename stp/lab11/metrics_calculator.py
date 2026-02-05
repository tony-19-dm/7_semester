import math
import json
from typing import Dict, List, Tuple


class MetricsCalculator:
    """
    Калькулятор метрических характеристик программ
    """
    
    @staticmethod
    def calculate_halstead_metrics(eta1: int, eta2: int, N1: int, N2: int) -> Dict[str, float]:
        """
        Расчет метрик Холстеда (для сравнения с нашей моделью)
        
        Args:
            eta1: число уникальных операторов
            eta2: число уникальных операндов
            N1: общее число операторов
            N2: общее число операндов
        
        Returns:
            Словарь с метриками Холстеда
        """
        # Словарь программы
        vocabulary = eta1 + eta2
        
        # Длина программы
        length = N1 + N2
        
        # Расчетная длина
        calculated_length = eta1 * math.log2(eta1) + eta2 * math.log2(eta2)
        
        # Объем программы
        volume = length * math.log2(vocabulary)
        
        # Сложность программы
        difficulty = (eta1 / 2) * (N2 / eta2) if eta2 > 0 else 0
        
        # Усилия по написанию
        effort = volume * difficulty
        
        # Время реализации (в секундах)
        time = effort / 18
        
        # Число ошибок
        bugs = volume / 3000
        
        return {
            'vocabulary': vocabulary,
            'length': length,
            'calculated_length': calculated_length,
            'volume': volume,
            'difficulty': difficulty,
            'effort': effort,
            'time_seconds': time,
            'estimated_bugs': bugs
        }
    
    @staticmethod
    def analyze_complexity(text: str) -> Dict[str, any]:
        """
        Анализ сложности текста программы
        
        Args:
            text: текст программы
        
        Returns:
            Словарь с характеристиками сложности
        """
        # Подсчет строк кода
        lines = text.split('\n')
        total_lines = len(lines)
        
        # Подсчет непустых строк
        non_empty_lines = sum(1 for line in lines if line.strip())
        
        # Подсчет строк с комментариями
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        # Подсчет циклов и условий
        control_structures = {
            'if': text.count(' if ') + text.count('\nif'),
            'for': text.count(' for ') + text.count('\nfor'),
            'while': text.count(' while ') + text.count('\nwhile'),
            'try': text.count(' try:') + text.count('\ntry:'),
            'except': text.count(' except') + text.count('\nexcept'),
            'def': text.count(' def ') + text.count('\ndef'),
            'class': text.count(' class ') + text.count('\nclass')
        }
        
        total_control_structures = sum(control_structures.values())
        
        # Цикломатическая сложность (упрощенная)
        # V(G) = P + 1, где P - число точек принятия решений
        cyclomatic_complexity = total_control_structures + 1
        
        return {
            'total_lines': total_lines,
            'non_empty_lines': non_empty_lines,
            'comment_lines': comment_lines,
            'comment_percentage': comment_lines / non_empty_lines * 100 if non_empty_lines > 0 else 0,
            'control_structures': control_structures,
            'total_control_structures': total_control_structures,
            'cyclomatic_complexity': cyclomatic_complexity
        }
    
    @staticmethod
    def compare_programs(program1_text: str, program2_text: str) -> Dict[str, any]:
        """
        Сравнение двух программ по метрическим характеристикам
        
        Args:
            program1_text: текст первой программы
            program2_text: текст второй программы
        
        Returns:
            Словарь с результатами сравнения
        """
        from model_programming import ProgrammingProcessModel
        
        model = ProgrammingProcessModel()
        
        # Анализ первой программы
        analysis1 = model.analyze_program_text(program1_text)
        metrics1 = MetricsCalculator.calculate_halstead_metrics(
            analysis1['unique_operators'],
            analysis1['unique_operands'],
            len([op for op in analysis1['operator_frequencies'].values()]),
            len([op for op in analysis1['operand_frequencies'].values()])
        )
        
        # Анализ второй программы
        analysis2 = model.analyze_program_text(program2_text)
        metrics2 = MetricsCalculator.calculate_halstead_metrics(
            analysis2['unique_operators'],
            analysis2['unique_operands'],
            len([op for op in analysis2['operator_frequencies'].values()]),
            len([op for op in analysis2['operand_frequencies'].values()])
        )
        
        # Сравнение
        comparison = {
            'program1': {
                'vocabulary': analysis1['vocabulary_size'],
                'length': analysis1['program_length'],
                'predicted_length': analysis1['predicted_length_2'],
                'error_percent': analysis1['relative_error_2'],
                'volume': metrics1['volume']
            },
            'program2': {
                'vocabulary': analysis2['vocabulary_size'],
                'length': analysis2['program_length'],
                'predicted_length': analysis2['predicted_length_2'],
                'error_percent': analysis2['relative_error_2'],
                'volume': metrics2['volume']
            },
            'differences': {
                'vocabulary_diff': analysis2['vocabulary_size'] - analysis1['vocabulary_size'],
                'length_diff': analysis2['program_length'] - analysis1['program_length'],
                'volume_diff': metrics2['volume'] - metrics1['volume'],
                'complexity_ratio': metrics2['difficulty'] / metrics1['difficulty'] if metrics1['difficulty'] > 0 else 0
            }
        }
        
        return comparison


def example_usage():
    """
    Пример использования метрик
    """
    # Пример простой программы
    simple_program = """
def add(a, b):
    result = a + b
    return result

def multiply(x, y):
    product = x * y
    return product

# Основная программа
if __name__ == "__main__":
    num1 = 10
    num2 = 20
    sum_result = add(num1, num2)
    prod_result = multiply(num1, num2)
    print(f"Sum: {sum_result}, Product: {prod_result}")
    """
    
    # Пример более сложной программы
    complex_program = """
import math
from typing import List, Tuple

class StatisticsCalculator:
    def __init__(self, data: List[float]):
        self.data = data
        self.sorted_data = sorted(data)
    
    def mean(self) -> float:
        if not self.data:
            return 0.0
        return sum(self.data) / len(self.data)
    
    def median(self) -> float:
        n = len(self.sorted_data)
        if n == 0:
            return 0.0
        if n % 2 == 1:
            return self.sorted_data[n // 2]
        else:
            mid = n // 2
            return (self.sorted_data[mid - 1] + self.sorted_data[mid]) / 2
    
    def variance(self) -> float:
        if len(self.data) < 2:
            return 0.0
        m = self.mean()
        return sum((x - m) ** 2 for x in self.data) / (len(self.data) - 1)
    
    def std_dev(self) -> float:
        return math.sqrt(self.variance())

# Использование
if __name__ == "__main__":
    numbers = [1.2, 2.3, 3.4, 4.5, 5.6]
    calc = StatisticsCalculator(numbers)
    
    print(f"Data: {numbers}")
    print(f"Mean: {calc.mean():.2f}")
    print(f"Median: {calc.median():.2f}")
    print(f"Variance: {calc.variance():.2f}")
    print(f"Std Dev: {calc.std_dev():.2f}")
    """
    
    calculator = MetricsCalculator()
    
    print("АНАЛИЗ ПРОСТОЙ ПРОГРАММЫ:")
    print("="*60)
    simple_complexity = calculator.analyze_complexity(simple_program)
    print(f"Строк кода: {simple_complexity['total_lines']}")
    print(f"Непустых строк: {simple_complexity['non_empty_lines']}")
    print(f"Цикломатическая сложность: {simple_complexity['cyclomatic_complexity']}")
    
    print("\nАНАЛИЗ СЛОЖНОЙ ПРОГРАММЫ:")
    print("="*60)
    complex_complexity = calculator.analyze_complexity(complex_program)
    print(f"Строк кода: {complex_complexity['total_lines']}")
    print(f"Непустых строк: {complex_complexity['non_empty_lines']}")
    print(f"Цикломатическая сложность: {complex_complexity['cyclomatic_complexity']}")
    
    print("\nСРАВНЕНИЕ ПРОГРАММ:")
    print("="*60)
    comparison = calculator.compare_programs(simple_program, complex_program)
    
    print(f"Словарь программы:")
    print(f"  Простая: {comparison['program1']['vocabulary']}")
    print(f"  Сложная: {comparison['program2']['vocabulary']}")
    print(f"  Разница: {comparison['differences']['vocabulary_diff']}")
    
    print(f"\nДлина программы:")
    print(f"  Простая: {comparison['program1']['length']}")
    print(f"  Сложная: {comparison['program2']['length']}")
    print(f"  Разница: {comparison['differences']['length_diff']}")
    
    print(f"\nОтносительная погрешность прогноза:")
    print(f"  Простая: {comparison['program1']['error_percent']:.2f}%")
    print(f"  Сложная: {comparison['program2']['error_percent']:.2f}%")


if __name__ == "__main__":
    example_usage()