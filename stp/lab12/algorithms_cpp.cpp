#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>

// 1. Поиск минимального элемента в 1D массиве
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

// 2. Сортировка пузырьком
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

// 3. Бинарный поиск
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
    
    return -1;  // Возвращаем -1 вместо nullptr
}

// 4. Поиск минимального элемента в 2D массиве
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

// 5. Разворот массива
std::vector<int> reverseArray(const std::vector<int>& arr) {
    std::vector<int> result = arr;
    int n = result.size();
    
    for (int i = 0; i < n / 2; i++) {
        std::swap(result[i], result[n - 1 - i]);
    }
    
    return result;
}

// 6. Циклический сдвиг влево
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

// 7. Замена всех вхождений
std::vector<int> replaceAll(const std::vector<int>& arr, int oldVal, int newVal) {
    std::vector<int> result = arr;
    
    for (int i = 0; i < result.size(); i++) {
        if (result[i] == oldVal) {
            result[i] = newVal;
        }
    }
    
    return result;
}

int main() {
    // Тестирование всех алгоритмов
    std::cout << "Testing algorithms in C++:" << std::endl;
    
    // Тест 1
    std::vector<int> arr1 = {5, 3, 8, 1, 9, 2};
    auto [minVal, minIdx] = findMin1D(arr1);
    std::cout << "1. Min in array: value=" << minVal << ", index=" << minIdx << std::endl;
    
    // Тест 2
    std::vector<int> arr2 = {64, 34, 25, 12, 22, 11, 90};
    auto sorted = bubbleSort(arr2);
    std::cout << "2. Sorted array: ";
    for (int val : sorted) std::cout << val << " ";
    std::cout << std::endl;
    
    return 0;
}