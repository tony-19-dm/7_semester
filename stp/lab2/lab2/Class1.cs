using System;

namespace MathOperations
{
    public static class ArrayProcessor
    {
        // 1. Поиск минимума из двух чисел
        public static double FindMin(double a, double b)
        {
            //if (a < b)
            //{
            //    return a;
            //}
            //else
            //{
            //    return b;
            //}

            return a < b ? a : b;
        }

        // 2. Поиск максимального значения во всем массиве
        public static double FindMaxInArray(double[,] A)
        {
            if (A == null)
                throw new ArgumentNullException(nameof(A), "Массив не может быть null");

            if (A.Length == 0)
                throw new ArgumentException("Массив не может быть пустым", nameof(A));

            double max = A[0, 0];
            int rows = A.GetLength(0);
            int cols = A.GetLength(1);

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    if (A[i, j] > max)
                    {
                        max = A[i, j];
                    }
                }
            }

            return max;
        }

        // 3. Поиск максимального значения на и выше побочной диагонали
        public static double FindMaxAboveSecondaryDiagonal(double[,] A)
        {
            if (A == null)
                throw new ArgumentNullException(nameof(A), "Массив не может быть null");

            if (A.Length == 0)
                throw new ArgumentException("Массив не может быть пустым", nameof(A));

            int rows = A.GetLength(0);
            int cols = A.GetLength(1);

            if (rows != cols)
                throw new ArgumentException("Массив должен быть квадратным", nameof(A));

            double max = double.MinValue;
            bool found = false;

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    // Условие для элементов на и выше побочной диагонали:
                    // i + j <= rows - 1
                    if (i + j <= rows - 1)
                    {
                        if (!found || A[i, j] > max)
                        {
                            max = A[i, j];
                            found = true;
                        }
                    }
                }
            }

            if (!found)
                throw new InvalidOperationException("Не найдено элементов на и выше побочной диагонали");

            return max;
        }
    }
}

