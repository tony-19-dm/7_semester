from typing import List, Tuple, Optional

# 1. Поиск минимального элемента в одномерном массиве
def find_min_1d(arr: List[int]) -> Tuple[Optional[int], Optional[int]]:
    """Возвращает (минимальное значение, индекс) или (None, None) если массив пуст"""
    if not arr:
        return None, None
    
    min_value = arr[0]
    min_index = 0
    
    for i in range(1, len(arr)):
        if arr[i] < min_value:
            min_value = arr[i]
            min_index = i
    
    return min_value, min_index

# 2. Сортировка пузырьком
def bubble_sort(arr: List[int]) -> None:
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

# 3. Бинарный поиск
def binary_search(arr: List[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # элемент не найден

# 4. Поиск минимального элемента в двумерном массиве
def find_min_2d(matrix: List[List[int]]) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """Возвращает (минимальное значение, строка, столбец)"""
    if not matrix or not matrix[0]:
        return None, None, None
    
    min_value = matrix[0][0]
    min_row, min_col = 0, 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < min_value:
                min_value = matrix[i][j]
                min_row, min_col = i, j
    
    return min_value, min_row, min_col

# 5. Перестановка элементов в обратном порядке
def reverse_array(arr: List[int]) -> None:
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# 6. Циклический сдвиг влево
def left_rotate(arr: List[int], positions: int) -> None:
    if not arr:
        return
    
    n = len(arr)
    positions = positions % n  # обработка случая, когда positions > n
    
    if positions == 0:
        return
    
    # Срезы Python делают это очень просто
    arr[:] = arr[positions:] + arr[:positions]
    
    # Альтернативная реализация без срезов:
    # def left_rotate_no_slices(arr, positions):
    #     n = len(arr)
    #     positions = positions % n
    #     
    #     # Переворачиваем первую часть
    #     for i in range(positions // 2):
    #         arr[i], arr[positions - i - 1] = arr[positions - i - 1], arr[i]
    #     
    #     # Переворачиваем вторую часть
    #     for i in range((n - positions) // 2):
    #         arr[positions + i], arr[n - i - 1] = arr[n - i - 1], arr[positions + i]
    #     
    #     # Переворачиваем весь массив
    #     for i in range(n // 2):
    #         arr[i], arr[n - i - 1] = arr[n - i - 1], arr[i]

# 7. Замена всех вхождений значения
def replace_all(arr: List[int], old_value: int, new_value: int) -> None:
    for i in range(len(arr)):
        if arr[i] == old_value:
            arr[i] = new_value

# Примеры использования функций
def demo_functions():
    # 1. Поиск минимального элемента
    arr1 = [5, 2, 8, 1, 9, 3]
    min_val, min_idx = find_min_1d(arr1)
    print(f"Минимальный элемент: {min_val} на позиции {min_idx}")
    
    # 2. Сортировка пузырьком
    arr2 = [5, 2, 8, 1, 9, 3]
    print(f"До сортировки: {arr2}")
    bubble_sort(arr2)
    print(f"После сортировки: {arr2}")
    
    # 3. Бинарный поиск
    sorted_arr = [1, 2, 3, 5, 8, 9]
    target = 5
    idx = binary_search(sorted_arr, target)
    print(f"Элемент {target} найден на позиции {idx}")
    
    # 4. Поиск в двумерном массиве
    matrix = [
        [5, 2, 8],
        [1, 9, 3],
        [4, 7, 6]
    ]
    min_val_2d, row, col = find_min_2d(matrix)
    print(f"Минимальный элемент 2D: {min_val_2d} на позиции ({row}, {col})")
    
    # 5. Реверс массива
    arr3 = [1, 2, 3, 4, 5]
    print(f"До реверса: {arr3}")
    reverse_array(arr3)
    print(f"После реверса: {arr3}")
    
    # 6. Циклический сдвиг
    arr4 = [1, 2, 3, 4, 5]
    print(f"До сдвига: {arr4}")
    left_rotate(arr4, 2)
    print(f"После сдвига на 2: {arr4}")
    
    # 7. Замена значений
    arr5 = [1, 2, 3, 2, 4, 2, 5]
    print(f"До замены: {arr5}")
    replace_all(arr5, 2, 99)
    print(f"После замены 2 на 99: {arr5}")

if __name__ == "__main__":
    demo_functions()