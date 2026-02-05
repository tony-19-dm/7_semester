using System;

namespace PathCoverage
{
    public static class PathOperations
    {
        // 1. Упорядочивание x, y, z в порядке убывания
        public static void SortDescending(ref int x, ref int y, ref int z)
        {
            if (x < y)
                Swap(ref x, ref y);
            if (x < z)
                Swap(ref x, ref z);
            if (y < z)
                Swap(ref y, ref z);
        }

        private static void Swap(ref int a, ref int b)
        {
            int temp = a;
            a = b;
            b = temp;
        }

        // 2. Наибольший общий делитель (алгоритм Евклида)
        public static int GCD(int a, int b)
        {
            if (a <= 0 || b <= 0)
                throw new ArgumentException("Числа должны быть положительными");
            while (b != 0){
                int temp = b;
                b = a % b;
                a = temp;}
            return a;
        }

        // 3. Формирование числа из четных разрядов
        public static int GetEvenDigits(int a)
        {
            if (a < 0) a = -a; // Работаем с модулем
            int result = 0;
            int position = 0;
            int temp = a;
            while (temp > 0){
                int digit = temp % 10;
                temp /= 10;
                position++;
                if (position % 2 == 0)
                    result = result * 10 + digit;}
            return ReverseNumber(result);
        }

        private static int ReverseNumber(int n)
        {
            int reversed = 0;
            while (n > 0){
                reversed = reversed * 10 + n % 10;
                n /= 10;}
            return reversed;
        }

        // 4. Сумма нечетных значений выше главной диагонали
        public static int SumOddAboveMainDiagonal(int[,] A)
        {
            if (A == null)
                throw new ArgumentNullException(nameof(A));
            int sum = 0;
            int rows = A.GetLength(0);
            int cols = A.GetLength(1);
            for (int i = 0; i < rows; i++){
                for (int j = 0; j < cols; j++){
                    if (j > i)
                        if (A[i, j] % 2 != 0)
                            sum += A[i, j];
                }
            }
            return sum;
        }
    }
}