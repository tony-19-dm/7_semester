from typing import List, Tuple, Optional, Any


def find_min_1d(arr: List[int]) -> Tuple[int, int]:
    """
    1. Отыскать минимальный элемент одномерного массива целых,
    его значение и значение его индекса.
    
    Args:
        arr: одномерный массив целых чисел
    
    Returns:
        Кортеж (значение, индекс)
    """
    if not arr:
        raise ValueError("Массив не может быть пустым")
    
    min_val = arr[0]
    min_idx = 0
    
    for i in range(1, len(arr)):
        if arr[i] < min_val:
            min_val = arr[i]
            min_idx = i
    
    return min_val, min_idx


def bubble_sort(arr: List[int]) -> List[int]:
    """
    2. Сортировка одномерного массива в порядке возрастания методом пузырька.
    
    Args:
        arr: массив для сортировки
    
    Returns:
        Отсортированный массив
    """
    n = len(arr)
    # Создаем копию массива, чтобы не изменять оригинал
    result = arr.copy()
    
    for i in range(n):
        # Флаг для оптимизации - если за проход не было перестановок, массив отсортирован
        swapped = False
        
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                # Меняем элементы местами
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        
        # Если перестановок не было, выходим
        if not swapped:
            break
    
    return result


def binary_search(arr: List[int], target: int) -> Optional[int]:
    """
    3. Бинарный поиск элемента в упорядоченном одномерном массиве.
    
    Args:
        arr: отсортированный массив
        target: искомый элемент
    
    Returns:
        Индекс элемента или None, если не найден
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def find_min_2d(matrix: List[List[int]]) -> Tuple[int, int, int]:
    """
    4. Отыскать минимальный элемент двумерного массива целых,
    его значение и значение его индексов.
    
    Args:
        matrix: двумерный массив
    
    Returns:
        Кортеж (значение, строка, столбец)
    """
    if not matrix or not matrix[0]:
        raise ValueError("Матрица не может быть пустой")
    
    min_val = matrix[0][0]
    min_row = 0
    min_col = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < min_val:
                min_val = matrix[i][j]
                min_row = i
                min_col = j
    
    return min_val, min_row, min_col


def reverse_array(arr: List[int]) -> List[int]:
    """
    5. Осуществить перестановку значений элементов
    одномерного массива в обратном порядке.
    
    Args:
        arr: массив для разворота
    
    Returns:
        Развернутый массив
    """
    result = arr.copy()
    n = len(result)
    
    for i in range(n // 2):
        result[i], result[n - 1 - i] = result[n - 1 - i], result[i]
    
    return result


def cyclic_shift_left(arr: List[int], k: int) -> List[int]:
    """
    6. Осуществлять циклический сдвиг элементов
    одномерного массива на заданное число позиций влево.
    
    Args:
        arr: исходный массив
        k: количество позиций для сдвига
    
    Returns:
        Массив после сдвига
    """
    if not arr:
        return []
    
    n = len(arr)
    k = k % n  # Обработка случая, когда k >= n
    
    if k == 0:
        return arr.copy()
    
    result = [0] * n
    
    for i in range(n):
        new_pos = (i - k) % n
        result[new_pos] = arr[i]
    
    return result


def replace_all(arr: List[int], old_val: int, new_val: int) -> List[int]:
    """
    7. Заменить все вхождения целочисленного значения в целочисленный массив.
    
    Args:
        arr: исходный массив
        old_val: значение для замены
        new_val: новое значение
    
    Returns:
        Массив с замененными значениями
    """
    result = arr.copy()
    
    for i in range(len(result)):
        if result[i] == old_val:
            result[i] = new_val
    
    return result


# Вспомогательные функции для тестирования
def test_algorithms():
    """Тестирование всех алгоритмов"""
    print("Тестирование алгоритмов:")
    print("=" * 50)
    
    # Тест 1: Поиск минимума в 1D массиве
    arr1 = [5, 3, 8, 1, 9, 2]
    min_val, min_idx = find_min_1d(arr1)
    print(f"1. Минимум в массиве {arr1}: значение={min_val}, индекс={min_idx}")
    
    # Тест 2: Сортировка пузырьком
    arr2 = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = bubble_sort(arr2)
    print(f"2. Сортировка {arr2}: {sorted_arr}")
    
    # Тест 3: Бинарный поиск
    arr3 = [1, 3, 5, 7, 9, 11, 13]
    target = 7
    idx = binary_search(arr3, target)
    print(f"3. Бинарный поиск {target} в {arr3}: индекс={idx}")
    
    # Тест 4: Поиск минимума в 2D массиве
    matrix = [
        [5, 3, 8],
        [1, 9, 2],
        [4, 7, 6]
    ]
    min_val_2d, row, col = find_min_2d(matrix)
    print(f"4. Минимум в матрице: значение={min_val_2d}, строка={row}, столбец={col}")
    
    # Тест 5: Разворот массива
    arr5 = [1, 2, 3, 4, 5]
    reversed_arr = reverse_array(arr5)
    print(f"5. Разворот {arr5}: {reversed_arr}")
    
    # Тест 6: Циклический сдвиг
    arr6 = [1, 2, 3, 4, 5]
    shifted = cyclic_shift_left(arr6, 2)
    print(f"6. Циклический сдвиг {arr6} на 2 влево: {shifted}")
    
    # Тест 7: Замена всех вхождений
    arr7 = [1, 2, 3, 2, 4, 2, 5]
    replaced = replace_all(arr7, 2, 99)
    print(f"7. Замена всех 2 на 99 в {arr7}: {replaced}")


if __name__ == "__main__":
    test_algorithms()