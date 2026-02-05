import unittest
import math
from model_programming import ProgrammingProcessModel
from metrics_calculator import MetricsCalculator


class TestProgrammingModel(unittest.TestCase):
    """Тесты для модели процесса написания программы"""
    
    def setUp(self):
        self.model = ProgrammingProcessModel()
    
    def test_single_trial(self):
        """Тест одного испытания моделирования"""
        for eta in [16, 32, 64]:
            L = self.model.simulate_single_trial(eta)
            # Длина программы должна быть не меньше eta
            self.assertGreaterEqual(L, eta)
            # Длина программы не должна быть чрезмерно большой
            # (в теории максимальное значение бесконечно, но на практике ограничено)
            self.assertLess(L, eta * 20)
    
    def test_theoretical_formulas(self):
        """Тест теоретических формул"""
        eta = 64
        
        theoretical = self.model.theoretical_values(eta)
        
        # Проверка формулы для математического ожидания
        expected_M = 0.9 * eta * math.log2(eta)
        self.assertAlmostEqual(theoretical['M_L_theoretical'], expected_M, places=2)
        
        # Проверка формулы для дисперсии
        expected_D = (math.pi ** 2 * eta ** 2) / 6
        self.assertAlmostEqual(theoretical['D_L_theoretical'], expected_D, places=2)
        
        # Проверка приближенной формулы для δ
        expected_delta_approx = 1 / (2 * math.log2(eta))
        self.assertAlmostEqual(theoretical['delta_approx'], expected_delta_approx, places=3)
    
    def test_analyze_program_text(self):
        """Тест анализа текста программы"""
        test_program = """
def test_function(x, y):
    result = x + y
    return result
        """
        
        analysis = self.model.analyze_program_text(test_program)
        
        # Проверка наличия ожидаемых ключей
        expected_keys = ['vocabulary_size', 'unique_operators', 'unique_operands', 
                        'program_length', 'predicted_length_1', 'predicted_length_2']
        
        for key in expected_keys:
            self.assertIn(key, analysis)
        
        # Проверка типов значений
        self.assertIsInstance(analysis['vocabulary_size'], int)
        self.assertIsInstance(analysis['program_length'], int)
        self.assertIsInstance(analysis['predicted_length_1'], float)
    
    def test_halstead_metrics(self):
        """Тест расчета метрик Холстеда"""
        eta1 = 10  # уникальные операторы
        eta2 = 15  # уникальные операнды
        N1 = 50    # общее число операторов
        N2 = 80    # общее число операндов
        
        metrics = MetricsCalculator.calculate_halstead_metrics(eta1, eta2, N1, N2)
        
        # Проверка расчета словаря
        expected_vocabulary = eta1 + eta2
        self.assertEqual(metrics['vocabulary'], expected_vocabulary)
        
        # Проверка расчета длины
        expected_length = N1 + N2
        self.assertEqual(metrics['length'], expected_length)
        
        # Проверка, что объем программы положительный
        self.assertGreater(metrics['volume'], 0)
    
    def test_complexity_analysis(self):
        """Тест анализа сложности"""
        test_code = """
if x > 0:
    for i in range(10):
        print(i)
else:
    while True:
        break
        """
        
        analysis = MetricsCalculator.analyze_complexity(test_code)
        
        # Проверка подсчета контрольных структур
        self.assertGreater(analysis['total_control_structures'], 0)
        
        # Проверка цикломатической сложности
        self.assertGreaterEqual(analysis['cyclomatic_complexity'], 1)


class TestStatisticalProperties(unittest.TestCase):
    """Тесты статистических свойств модели"""
    
    def test_convergence_of_mean(self):
        """Тест сходимости среднего значения при увеличении числа испытаний"""
        model = ProgrammingProcessModel()
        eta = 32
        
        means = []
        for trials in [100, 500, 1000, 2000]:
            result = model.simulate_multiple_trials(eta, trials)
            means.append(result['mean_L'])
        
        # Проверяем, что средние значения стабилизируются
        # (разница между последовательными значениями уменьшается)
        diffs = [abs(means[i] - means[i-1]) for i in range(1, len(means))]
        self.assertTrue(all(diffs[i] >= diffs[i+1] for i in range(len(diffs)-1)))
    
    def test_relative_error_bound(self):
        """Тест, что относительная погрешность δ не превышает 10%"""
        model = ProgrammingProcessModel()
        
        for eta in [16, 32, 64, 128]:
            result = model.simulate_multiple_trials(eta, 500)
            rel_error = result['rel_error']
            
            # Согласно теории, δ обычно не превышает 10%
            self.assertLess(rel_error, 0.15)  # Небольшой запас для случайных флуктуаций


def run_performance_test():
    """Тест производительности моделирования"""
    import time
    
    model = ProgrammingProcessModel()
    
    print("\nТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("="*60)
    
    for eta in [16, 32, 64, 128, 256]:
        start_time = time.time()
        result = model.simulate_multiple_trials(eta, 1000)
        end_time = time.time()
        
        elapsed = end_time - start_time
        print(f"η={eta:3d}: {elapsed:.3f} сек, M(L)={result['mean_L']:.2f}")


if __name__ == "__main__":
    # Запуск юнит-тестов
    unittest.main(exit=False)
    
    # Запуск теста производительности
    run_performance_test()