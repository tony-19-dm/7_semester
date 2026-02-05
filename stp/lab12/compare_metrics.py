import math
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt


def compare_languages():
    """
    Сравнение метрик для Python и C++ реализаций
    """
    
    # Формат: (алгоритм, η1, η2, N1, N2, η2_star)
    cpp_metrics = [
        ("findMin1D", 8, 12, 25, 30, 1),   # 1 параметр (массив)
        ("bubbleSort", 10, 15, 35, 45, 1), # 1 параметр
        ("binarySearch", 9, 13, 28, 35, 2), # 2 параметра (массив, цель)
        ("findMin2D", 9, 14, 30, 40, 1),   # 1 параметр
        ("reverseArray", 7, 10, 20, 25, 1), # 1 параметр
        ("cyclicShiftLeft", 8, 13, 26, 32, 2), # 2 параметра
        ("replaceAll", 8, 12, 24, 30, 3),  # 3 параметра
    ]
    
    # Метрики для Python
    python_metrics = [
        ("find_min_1d", 7, 10, 22, 28, 1),
        ("bubble_sort", 9, 13, 32, 40, 1),
        ("binary_search", 8, 11, 25, 32, 2),
        ("find_min_2d", 8, 12, 28, 36, 1),
        ("reverse_array", 6, 9, 18, 22, 1),
        ("cyclic_shift_left", 7, 11, 23, 29, 2),
        ("replace_all", 7, 10, 21, 27, 3),
    ]
    
    def calculate_v(η: int, N: int) -> float:
        """Расчет объема реализации"""
        if η > 0:
            return N * math.log2(η)
        return 0
    
    def calculate_l_hat(η1: int, η2: int, N2: int) -> float:
        """Расчет уровня программы по реализации"""
        if η1 > 0 and N2 > 0:
            return (2 / η1) * (η2 / N2)
        return 0
    
    # Расчет метрик для C++
    cpp_results = []
    for name, η1, η2, N1, N2, η2_star in cpp_metrics:
        η = η1 + η2
        N = N1 + N2
        V = calculate_v(η, N)
        L_hat = calculate_l_hat(η1, η2, N2)
        λ1 = (L_hat ** 2) * V
        
        cpp_results.append({
            'name': name,
            'η1': η1,
            'η2': η2,
            'N': N,
            'V': V,
            'L_hat': L_hat,
            'λ1': λ1
        })
    
    # Расчет метрик для Python
    python_results = []
    for name, η1, η2, N1, N2, η2_star in python_metrics:
        η = η1 + η2
        N = N1 + N2
        V = calculate_v(η, N)
        L_hat = calculate_l_hat(η1, η2, N2)
        λ1 = (L_hat ** 2) * V
        
        python_results.append({
            'name': name,
            'η1': η1,
            'η2': η2,
            'N': N,
            'V': V,
            'L_hat': L_hat,
            'λ1': λ1
        })
    
    # Сравнительная таблица
    print("\n" + "="*100)
    print("СРАВНЕНИЕ МЕТРИЧЕСКИХ ХАРАКТЕРИСТИК PYTHON И C++ РЕАЛИЗАЦИЙ")
    print("="*100)
    
    headers = ["Алгоритм", "Язык", "η1", "η2", "N", "V", "L^", "λ1"]
    print(f"{headers[0]:<20} {headers[1]:<10} {headers[2]:>4} {headers[3]:>4} "
          f"{headers[4]:>6} {headers[5]:>8} {headers[6]:>8} {headers[7]:>8}")
    print("-"*100)
    
    for i in range(len(cpp_results)):
        cpp = cpp_results[i]
        py = python_results[i]
        
        print(f"{cpp['name']:<20} {'C++':<10} {cpp['η1']:>4.0f} {cpp['η2']:>4.0f} "
              f"{cpp['N']:>6.0f} {cpp['V']:>8.2f} {cpp['L_hat']:>8.4f} {cpp['λ1']:>8.4f}")
        
        print(f"{py['name']:<20} {'Python':<10} {py['η1']:>4.0f} {py['η2']:>4.0f} "
              f"{py['N']:>6.0f} {py['V']:>8.2f} {py['L_hat']:>8.4f} {py['λ1']:>8.4f}")
        print("-"*100)
    
    # Статистика сравнения
    print("\nСРАВНИТЕЛЬНАЯ СТАТИСТИКА:")
    print("-"*50)
    
    # Средние значения
    avg_v_cpp = sum(r['V'] for r in cpp_results) / len(cpp_results)
    avg_v_py = sum(r['V'] for r in python_results) / len(python_results)
    
    avg_λ1_cpp = sum(r['λ1'] for r in cpp_results) / len(cpp_results)
    avg_λ1_py = sum(r['λ1'] for r in python_results) / len(python_results)
    
    print(f"Средний объем реализации (V):")
    print(f"  C++:    {avg_v_cpp:.2f}")
    print(f"  Python: {avg_v_py:.2f}")
    print(f"  Отношение (C++/Python): {avg_v_cpp/avg_v_py:.2f}")
    
    print(f"\nСредний уровень языка (λ1):")
    print(f"  C++:    {avg_λ1_cpp:.4f}")
    print(f"  Python: {avg_λ1_py:.4f}")
    print(f"  Отношение (C++/Python): {avg_λ1_cpp/avg_λ1_py:.2f}")
    
    # Визуализация сравнения
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Данные для графиков
    algorithm_names = [r['name'] for r in cpp_results]
    cpp_V = [r['V'] for r in cpp_results]
    py_V = [r['V'] for r in python_results]
    
    cpp_λ1 = [r['λ1'] for r in cpp_results]
    py_λ1 = [r['λ1'] for r in python_results]
    
    # График 1: Объем реализации
    ax1 = axes[0, 0]
    x = range(len(algorithm_names))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], cpp_V, width, label='C++', alpha=0.8)
    ax1.bar([i + width/2 for i in x], py_V, width, label='Python', alpha=0.8)
    ax1.set_xlabel('Алгоритм')
    ax1.set_ylabel('Объем реализации (V)')
    ax1.set_title('Сравнение объема реализации')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algorithm_names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # График 2: Уровень языка λ1
    ax2 = axes[0, 1]
    ax2.bar([i - width/2 for i in x], cpp_λ1, width, label='C++', alpha=0.8)
    ax2.bar([i + width/2 for i in x], py_λ1, width, label='Python', alpha=0.8)
    ax2.set_xlabel('Алгоритм')
    ax2.set_ylabel('Уровень языка (λ1)')
    ax2.set_title('Сравнение уровня языка программирования')
    ax2.set_xticks(x)
    ax2.set_xticklabels(algorithm_names, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # График 3: Отношение метрик
    ax3 = axes[1, 0]
    ratio_V = [cpp_V[i]/py_V[i] for i in range(len(cpp_V))]
    ratio_λ1 = [cpp_λ1[i]/py_λ1[i] for i in range(len(cpp_λ1))]
    
    ax3.plot(algorithm_names, ratio_V, 'bo-', label='V(C++)/V(Python)', linewidth=2)
    ax3.plot(algorithm_names, ratio_λ1, 'ro-', label='λ1(C++)/λ1(Python)', linewidth=2)
    ax3.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Алгоритм')
    ax3.set_ylabel('Отношение метрик')
    ax3.set_title('Отношение метрик C++ к Python')
    ax3.set_xticklabels(algorithm_names, rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # График 4: Корреляция
    ax4 = axes[1, 1]
    ax4.scatter(cpp_V, py_V, s=100, alpha=0.7)
    
    # Линия равенства
    max_val = max(max(cpp_V), max(py_V))
    ax4.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Линия равенства')
    
    # Подписи точек
    for i, name in enumerate(algorithm_names):
        ax4.annotate(name, (cpp_V[i], py_V[i]), fontsize=8)
    
    ax4.set_xlabel('Объем C++ реализации (V)')
    ax4.set_ylabel('Объем Python реализации (V)')
    ax4.set_title('Корреляция объемов реализации')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('language_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*100)
    print("ВЫВОДЫ ПО СРАВНЕНИЮ ЯЗЫКОВ:")
    print("="*100)
    print("1. Объем реализации (V) в C++ обычно больше, чем в Python.")
    print("2. Это связано с более низкоуровневой природой C++ и необходимостью")
    print("   явного объявления типов и управления памятью.")
    print("3. Уровень языка (λ1) также различается, что отражает разные парадигмы")
    print("   и выразительные возможности языков.")
    print("4. Python демонстрирует более высокий уровень абстракции, что")
    print("   приводит к меньшему объему кода для решения тех же задач.")
    print("5. Метрики позволяют количественно оценить различия между языками")
    print("   и выбрать подходящий язык для конкретной задачи.")


if __name__ == "__main__":
    compare_languages()