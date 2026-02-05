#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 1. Поиск минимального элемента в одномерном массиве
void findMin1D(int arr[], int size, int& minValue, int& minIndex) {
    if (size == 0) {
        minValue = -1;
        minIndex = -1;
        return;
    }
    
    minValue = arr[0];
    minIndex = 0;
    
    for (int i = 1; i < size; i++) {
        if (arr[i] < minValue) {
            minValue = arr[i];
            minIndex = i;
        }
    }
}

// 2. Сортировка пузырьком
void bubbleSort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// 3. Бинарный поиск
int binarySearch(int arr[], int size, int target) {
    int left = 0, right = size - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        }
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1; // элемент не найден
}

// 4. Поиск минимального элемента в двумерном массиве
void findMin2D(vector<vector<int>>& matrix, int& minValue, int& minRow, int& minCol) {
    if (matrix.empty() || matrix[0].empty()) {
        minValue = -1;
        minRow = -1;
        minCol = -1;
        return;
    }
    
    minValue = matrix[0][0];
    minRow = 0;
    minCol = 0;
    
    for (int i = 0; i < matrix.size(); i++) {
        for (int j = 0; j < matrix[i].size(); j++) {
            if (matrix[i][j] < minValue) {
                minValue = matrix[i][j];
                minRow = i;
                minCol = j;
            }
        }
    }
}

// 5. Перестановка элементов в обратном порядке
void reverseArray(int arr[], int size) {
    for (int i = 0; i < size / 2; i++) {
        swap(arr[i], arr[size - i - 1]);
    }
}

// 6. Циклический сдвиг влево
void leftRotate(int arr[], int size, int positions) {
    if (size == 0) return;
    
    positions = positions % size; // обработка случая, когда positions > size
    if (positions == 0) return;
    
    // Временный массив для хранения первых positions элементов
    int* temp = new int[positions];
    
    // Сохраняем первые positions элементов
    for (int i = 0; i < positions; i++) {
        temp[i] = arr[i];
    }
    
    // Сдвигаем остальные элементы влево
    for (int i = positions; i < size; i++) {
        arr[i - positions] = arr[i];
    }
    
    // Восстанавливаем сохраненные элементы в конец
    for (int i = 0; i < positions; i++) {
        arr[size - positions + i] = temp[i];
    }
    
    delete[] temp;
}

// 7. Замена всех вхождений значения
void replaceAll(int arr[], int size, int oldValue, int newValue) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == oldValue) {
            arr[i] = newValue;
        }
    }
}

// Вспомогательная функция для печати массива
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}