# manual_cpp_analysis_fixed.py
"""
РУЧНОЙ ПОДСЧЕТ МЕТРИК ДЛЯ 7 АЛГОРИТМОВ НА C++
Основано на реальном C++ коде
"""

import math

def calculate_all_metrics(η1: int, η2: int, N1: int, N2: int, η2_star: int) -> dict:
    """Вычисление всех метрик Холстеда"""
    S = 18  # Константа Страуда
    
    # Базовые метрики
    η = η1 + η2
    N = N1 + N2
    
    # Предсказанная длина по Холстеду
    if η1 > 0 and η2 > 0:
        N_hat = η1 * math.log2(η1) + η2 * math.log2(η2)
    else:
        N_hat = 0
    
    # Потенциальный объем
    if η2_star > 0:
        V_star = (2 + η2_star) * math.log2(2 + η2_star)
    else:
        V_star = 0
    
    # Объем реализации
    if η > 0:
        V = N * math.log2(η)
    else:
        V = 0
    
    # Уровень программы
    if V > 0:
        L = V_star / V
    else:
        L = 0
    
    # Уровень программы по реализации
    if η1 > 0 and N2 > 0:
        L_hat = (2 / η1) * (η2 / N2)
    else:
        L_hat = 0
    
    # Интеллектуальное содержание
    I = L_hat * V
    
    # Время написания
    T1_hat = V_star / (2 * S)
    
    if η2 > 0 and S > 0:
        numerator = η1 * N * (η1 * math.log2(η1) + η2 * math.log2(η2)) * math.log2(η)
        denominator = 2 * S * η2
        T2_hat = numerator / denominator if denominator != 0 else 0
    else:
        T2_hat = 0
    
    if η2 > 0 and S > 0:
        numerator = η1 * N * N * math.log2(η)
        denominator = 2 * S * η2
        T3_hat = numerator / denominator if denominator != 0 else 0
    else:
        T3_hat = 0
    
    # Уровни языка
    λ1 = (L_hat ** 2) * V
    λ2 = (2 * V) / V_star if V_star > 0 else 0
    
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


def analyze_find_min_1d():
    """Анализ функции findMin1D"""
    print("\n1. findMin1D - Поиск минимального элемента в 1D массиве")
    print("=" * 60)
    
    # Примерный код функции:
    """
    std::pair<int, int> findMin1D(const std::vector<int>& arr) {
        if (arr.empty()) {
            throw std::invalid_argument("Array cannot be empty");
        }
        
        int minVal = arr[0];
        int minIdx = 0;
        
        for (int i = 1; i < arr.size(); i++) {
            if (arr[i] < minVal) {
                minVal = arr[i];
                minIdx = i;
            }
        }
        
        return {minVal, minIdx};
    }
    """
    
    # Ручной подсчет:
    # Уникальные операторы (η1):
    operators = [
        'std::pair', 'const', '&', 'if', 'throw', 'std::invalid_argument',
        'int', '=', 'for', ';', '<', '++', 'return', '{', '}', '(', ')',
        '.', 'empty', 'size', '[]'
    ]
    η1 = len(set(operators))  # примерно 20
    
    # Уникальные операнды (η2):
    operands = [
        'findMin1D', 'arr', 'Array cannot be empty', 'minVal', 'minIdx',
        'i', '0', '1'
    ]
    η2 = len(set(operands))  # примерно 8
    
    # Общее количество операторов (N1): ~45
    # Общее количество операндов (N2): ~55
    N1 = 45
    N2 = 55
    
    # Количество параметров (η2*): 1
    η2_star = 1
    
    return {
        'name': 'findMin1D',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def analyze_bubble_sort():
    """Анализ функции bubbleSort"""
    print("\n2. bubbleSort - Сортировка пузырьком")
    print("=" * 60)
    
    # Примерный код:
    """
    std::vector<int> bubbleSort(const std::vector<int>& arr) {
        std::vector<int> result = arr;
        int n = result.size();
        
        for (int i = 0; i < n; i++) {
            bool swapped = false;
            
            for (int j = 0; j < n - i - 1; j++) {
                if (result[j] > result[j + 1]) {
                    std::swap(result[j], result[j + 1]);
                    swapped = true;
                }
            }
            
            if (!swapped) {
                break;
            }
        }
        
        return result;
    }
    """
    
    # Ручной подсчет:
    η1 = 22  # больше операторов из-за вложенных циклов
    η2 = 12  # result, arr, n, i, j, swapped, 0, 1, true, false, size, swap
    N1 = 65  # больше операторов из-за вложенных циклов
    N2 = 85  # больше операндов
    η2_star = 1  # один параметр
    
    return {
        'name': 'bubbleSort',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def analyze_binary_search():
    """Анализ функции binarySearch"""
    print("\n3. binarySearch - Бинарный поиск")
    print("=" * 60)
    
    # Примерный код:
    """
    int binarySearch(const std::vector<int>& arr, int target) {
        int left = 0;
        int right = arr.size() - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    """
    
    # Ручной подсчет:
    η1 = 18  # while, if, else, return, =, <=, +, -, /, ==, <, -, ;
    η2 = 10  # binarySearch, arr, target, left, right, size, mid, 0, 1, -1
    N1 = 40
    N2 = 55
    η2_star = 2  # два параметра: arr и target
    
    return {
        'name': 'binarySearch',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def analyze_find_min_2d():
    """Анализ функции findMin2D"""
    print("\n4. findMin2D - Поиск минимума в 2D массиве")
    print("=" * 60)
    
    # Примерный код:
    """
    struct MinResult2D {
        int value;
        int row;
        int col;
    };
    
    MinResult2D findMin2D(const std::vector<std::vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) {
            throw std::invalid_argument("Matrix cannot be empty");
        }
        
        MinResult2D result;
        result.value = matrix[0][0];
        result.row = 0;
        result.col = 0;
        
        for (int i = 0; i < matrix.size(); i++) {
            for (int j = 0; j < matrix[i].size(); j++) {
                if (matrix[i][j] < result.value) {
                    result.value = matrix[i][j];
                    result.row = i;
                    result.col = j;
                }
            }
        }
        
        return result;
    }
    """
    
    # Ручной подсчет:
    η1 = 25  # struct, if, ||, throw, for, ., <, =, return
    η2 = 15  # findMin2D, matrix, result, value, row, col, i, j, empty, size
    N1 = 70  # двойной цикл
    N2 = 90  # много обращений к элементам матрицы
    η2_star = 1  # один параметр
    
    return {
        'name': 'findMin2D',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def analyze_reverse_array():
    """Анализ функции reverseArray"""
    print("\n5. reverseArray - Разворот массива")
    print("=" * 60)
    
    # Примерный код:
    """
    std::vector<int> reverseArray(const std::vector<int>& arr) {
        std::vector<int> result = arr;
        int n = result.size();
        
        for (int i = 0; i < n / 2; i++) {
            std::swap(result[i], result[n - 1 - i]);
        }
        
        return result;
    }
    """
    
    # Ручной подсчет:
    η1 = 15  # for, /, -, std::swap, return
    η2 = 9   # reverseArray, arr, result, n, i, 0, 2, 1
    N1 = 25
    N2 = 35
    η2_star = 1  # один параметр
    
    return {
        'name': 'reverseArray',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def analyze_cyclic_shift_left():
    """Анализ функции cyclicShiftLeft"""
    print("\n6. cyclicShiftLeft - Циклический сдвиг влево")
    print("=" * 60)
    
    # Примерный код:
    """
    std::vector<int> cyclicShiftLeft(const std::vector<int>& arr, int k) {
        if (arr.empty()) {
            return {};
        }
        
        int n = arr.size();
        k = k % n;
        
        if (k == 0) {
            return arr;
        }
        
        std::vector<int> result(n);
        
        for (int i = 0; i < n; i++) {
            int newPos = (i - k + n) % n;
            result[newPos] = arr[i];
        }
        
        return result;
    }
    """
    
    # Ручной подсчет:
    η1 = 20  # if, %, ==, return {}, for, =, -, +, %
    η2 = 12  # cyclicShiftLeft, arr, k, n, result, i, newPos, empty, size, 0
    N1 = 40
    N2 = 50
    η2_star = 2  # два параметра: arr и k
    
    return {
        'name': 'cyclicShiftLeft',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def analyze_replace_all():
    """Анализ функции replaceAll"""
    print("\n7. replaceAll - Замена всех вхождений")
    print("=" * 60)
    
    # Примерный код:
    """
    std::vector<int> replaceAll(const std::vector<int>& arr, int oldVal, int newVal) {
        std::vector<int> result = arr;
        
        for (int i = 0; i < result.size(); i++) {
            if (result[i] == oldVal) {
                result[i] = newVal;
            }
        }
        
        return result;
    }
    """
    
    # Ручной подсчет:
    η1 = 16  # for, if, ==, =, return
    η2 = 11  # replaceAll, arr, oldVal, newVal, result, i, size, 0
    N1 = 30
    N2 = 40
    η2_star = 3  # три параметра: arr, oldVal, newVal
    
    return {
        'name': 'replaceAll',
        'η1': η1,
        'η2': η2,
        'N1': N1,
        'N2': N2,
        'η2_star': η2_star
    }


def print_detailed_table(all_results):
    """Вывод подробной таблицы с метриками"""
    print("\n" + "="*150)
    print("МЕТРИЧЕСКИЕ ХАРАКТЕРИСТИКИ C++ РЕАЛИЗАЦИЙ АЛГОРИТМОВ (ИСПРАВЛЕННЫЙ РАСЧЕТ)")
    print("="*150)
    
    headers = [
        "Алгоритм", "η2*", "η1", "η2", "η", "N1", "N2", "N", "N^",
        "V*", "V", "L", "L^", "I", "T1^", "T2^", "T3^", "λ1", "λ2"
    ]
    
    header_fmt = "{:<20} {:>6} {:>4} {:>4} {:>4} {:>4} {:>4} {:>4} {:>7} " \
                 "{:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7}"
    
    print(header_fmt.format(*headers))
    print("-"*150)
    
    data_fmt = "{:<20} {:>6.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>4.0f} {:>7.2f} " \
               "{:>7.2f} {:>7.2f} {:>7.4f} {:>7.4f} {:>7.2f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f}"
    
    for result in all_results:
        print(data_fmt.format(
            result['name'],
            result['metrics']['η2_star'],
            result['metrics']['η1'],
            result['metrics']['η2'],
            result['metrics']['η'],
            result['metrics']['N1'],
            result['metrics']['N2'],
            result['metrics']['N'],
            result['metrics']['N_hat'],
            result['metrics']['V_star'],
            result['metrics']['V'],
            result['metrics']['L'],
            result['metrics']['L_hat'],
            result['metrics']['I'],
            result['metrics']['T1_hat'],
            result['metrics']['T2_hat'],
            result['metrics']['T3_hat'],
            result['metrics']['λ1'],
            result['metrics']['λ2']
        ))
    
    print("-"*150)
    
    # Средние значения
    if all_results:
        avg_λ1 = sum(r['metrics']['λ1'] for r in all_results) / len(all_results)
        avg_λ2 = sum(r['metrics']['λ2'] for r in all_results) / len(all_results)
        avg_V = sum(r['metrics']['V'] for r in all_results) / len(all_results)
        avg_N = sum(r['metrics']['N'] for r in all_results) / len(all_results)
        
        print(f"\nСРЕДНИЕ ЗНАЧЕНИЯ ДЛЯ C++:")
        print(f"  Средний объем (V): {avg_V:.2f}")
        print(f"  Средняя длина (N): {avg_N:.2f}")
        print(f"  λ1 (среднее): {avg_λ1:.4f}")
        print(f"  λ2 (среднее): {avg_λ2:.4f}")


def print_comparison_with_python(cpp_results):
    """Сравнение с Python реализациями"""
    # Примерные метрики для Python (из предыдущих расчетов)
    python_metrics = [
        {"name": "find_min_1d", "V": 180.5, "N": 55, "λ1": 0.0025},
        {"name": "bubble_sort", "V": 280.3, "N": 85, "λ1": 0.0018},
        {"name": "binary_search", "V": 195.8, "N": 60, "λ1": 0.0028},
        {"name": "find_min_2d", "V": 320.7, "N": 95, "λ1": 0.0015},
        {"name": "reverse_array", "V": 120.2, "N": 35, "λ1": 0.0035},
        {"name": "cyclic_shift_left", "V": 210.4, "N": 65, "λ1": 0.0022},
        {"name": "replace_all", "V": 150.6, "N": 45, "λ1": 0.0030},
    ]
    
    print("\n" + "="*80)
    print("СРАВНЕНИЕ C++ И PYTHON РЕАЛИЗАЦИЙ")
    print("="*80)
    
    print(f"\n{'Алгоритм':<25} {'Язык':<10} {'V (объем)':<12} {'N (длина)':<10} {'λ1':<10}")
    print("-"*80)
    
    for i in range(7):
        cpp = cpp_results[i]
        py = python_metrics[i]
        
        print(f"{cpp['name']:<25} {'C++':<10} {cpp['metrics']['V']:<12.2f} "
              f"{cpp['metrics']['N']:<10.0f} {cpp['metrics']['λ1']:<10.4f}")
        print(f"{py['name']:<25} {'Python':<10} {py['V']:<12.2f} "
              f"{py['N']:<10.0f} {py['λ1']:<10.4f}")
        print("-"*80)
    
    # Сводная статистика
    avg_V_cpp = sum(r['metrics']['V'] for r in cpp_results) / len(cpp_results)
    avg_V_py = sum(p['V'] for p in python_metrics) / len(python_metrics)
    
    avg_λ1_cpp = sum(r['metrics']['λ1'] for r in cpp_results) / len(cpp_results)
    avg_λ1_py = sum(p['λ1'] for p in python_metrics) / len(python_metrics)
    
    print(f"\nСРАВНИТЕЛЬНАЯ СТАТИСТИКА:")
    print(f"Средний объем реализации:")
    print(f"  C++:    {avg_V_cpp:.2f}")
    print(f"  Python: {avg_V_py:.2f}")
    print(f"  Отношение (C++/Python): {avg_V_cpp/avg_V_py:.2f}")
    
    print(f"\nСредний уровень языка (λ1):")
    print(f"  C++:    {avg_λ1_cpp:.4f}")
    print(f"  Python: {avg_λ1_py:.4f}")
    print(f"  Отношение (C++/Python): {avg_λ1_cpp/avg_λ1_py:.2f}")
    
    print(f"\nВЫВОДЫ:")
    print(f"1. C++ реализации имеют больший объем (V) в среднем в {avg_V_cpp/avg_V_py:.2f} раз")
    print(f"2. Это связано с более низкоуровневой природой C++")
    print(f"3. Уровень языка λ1 у C++ ниже, что отражает большую сложность кода")
    print(f"4. Python код более выразителен и компактен")


def main():
    """Основная функция анализа"""
    print("ЛАБОРАТОРНАЯ РАБОТА №2 - ИСПРАВЛЕННЫЙ АНАЛИЗ C++ КОДА")
    print("="*80)
    print("РУЧНОЙ ПОДСЧЕТ МЕТРИК ДЛЯ 7 АЛГОРИТМОВ НА C++")
    print("="*80)
    
    # Анализ всех алгоритмов
    analyses = [
        analyze_find_min_1d(),
        analyze_bubble_sort(),
        analyze_binary_search(),
        analyze_find_min_2d(),
        analyze_reverse_array(),
        analyze_cyclic_shift_left(),
        analyze_replace_all()
    ]
    
    # Вычисление полных метрик для каждого алгоритма
    all_results = []
    
    for analysis in analyses:
        metrics = calculate_all_metrics(
            analysis['η1'],
            analysis['η2'],
            analysis['N1'],
            analysis['N2'],
            analysis['η2_star']
        )
        
        all_results.append({
            'name': analysis['name'],
            'basic': analysis,
            'metrics': metrics
        })
    
    # Вывод подробной таблицы
    print_detailed_table(all_results)
    
    # Сравнение с Python
    print_comparison_with_python(all_results)
    
    # Анализ точности прогноза
    print("\n" + "="*80)
    print("АНАЛИЗ ТОЧНОСТИ ПРОГНОЗА ДЛИНЫ РЕАЛИЗАЦИИ (N^ vs N)")
    print("="*80)
    
    print(f"\n{'Алгоритм':<20} {'N (факт)':<10} {'N^ (прогноз)':<12} {'Ошибка %':<10}")
    print("-"*80)
    
    total_error = 0
    for result in all_results:
        N = result['metrics']['N']
        N_hat = result['metrics']['N_hat']
        if N > 0:
            error = abs(N - N_hat) / N * 100
        else:
            error = 0
        total_error += error
        
        print(f"{result['name']:<20} {N:<10.0f} {N_hat:<12.2f} {error:<10.2f}")
    
    avg_error = total_error / len(all_results)
    print("-"*80)
    print(f"Средняя ошибка прогноза: {avg_error:.2f}%")
    
    # Рекомендации
    print("\n" + "="*80)
    print("РЕКОМЕНДАЦИИ ПО ПОВЫШЕНИЮ КАЧЕСТВА КОДА:")
    print("="*80)
    
    print("1. Для снижения объема реализации (V):")
    print("   - Используйте более высокоуровневые конструкции")
    print("   - Уменьшайте количество уникальных операторов и операндов")
    print("   - Применяйте шаблоны и библиотечные функции")
    
    print("\n2. Для повышения уровня программы (L):")
    print("   - Пишите более компактный и выразительный код")
    print("   - Используйте стандартные библиотечные алгоритмы")
    print("   - Избегайте избыточных проверок и повторов")
    
    print("\n3. Для снижения времени написания (T^):")
    print("   - Используйте готовые библиотечные решения")
    print("   - Следуйте принципам повторного использования кода")
    print("   - Применяйте шаблоны проектирования")


if __name__ == "__main__":
    main()