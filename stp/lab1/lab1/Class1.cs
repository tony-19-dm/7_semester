namespace NumberConverter
{
    public static class Class1
    {

        static public double MultiplyINdex(double[] arr)
        {
            if (arr == null || arr.Length < 2)
            {
                return 0;
            }
            double product = 1.0;

            for (int i = 1; i < arr.Length; i += 2)
            {
                product *= arr[i];
            }

            return product;
        }

        public static void CyclicShiftRight(double[] array, int shift)
        {
            if (array == null || array.Length == 0)
                return;

            // Нормализуем сдвиг (если сдвиг больше длины массива)
            shift = shift % array.Length;
            if (shift == 0) return; // Сдвиг не нужен

            // Создаем временный массив для хранения элементов
            double[] temp = new double[shift];

            // Сохраняем последние 'shift' элементов
            Array.Copy(array, array.Length - shift, temp, 0, shift);

            // Сдвигаем остальные элементы вправо
            for (int i = array.Length - 1; i >= shift; i--)
            {
                array[i] = array[i - shift];
            }

            // Восстанавливаем сохраненные элементы в начало
            Array.Copy(temp, 0, array, 0, shift);
        }

        public static double FractionFromString(int b, string s)
        {
            if (b < 2 || b > 16)
                throw new ArgumentException("Основание должно быть от 2 до 16");

            if (string.IsNullOrEmpty(s))
                return 0.0;

            double fraction = 0.0;
            double divisor = 1.0 / b;

            foreach (char c in s)
            {
                int digitValue = char.IsDigit(c) ? c - '0' : char.ToUpper(c) - 'A' + 10;

                if (digitValue >= b)
                    throw new ArgumentException($"Цифра {c} недопустима для системы с основанием {b}");

                fraction += digitValue * divisor;
                divisor /= b;
            }

            return fraction;
        }
    }
}