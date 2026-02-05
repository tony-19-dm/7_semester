using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace PathCoverage.Tests
{
    [TestClass]
    public class PathOperationsC2Tests
    {
        // ==================== SortDescending ====================

        [TestMethod]
        public void SortDescending_AlreadySorted_NoChanges()
        {
            // Путь: все условия false
            int x = 3, y = 2, z = 1;
            int expectedX = 3, expectedY = 2, expectedZ = 1;

            PathOperations.SortDescending(ref x, ref y, ref z);

            Assert.AreEqual(expectedX, x);
            Assert.AreEqual(expectedY, y);
            Assert.AreEqual(expectedZ, z);
        }

        [TestMethod]
        public void SortDescending_ReverseOrder_FullSwap()
        {
            // Путь: все условия true
            int x = 1, y = 2, z = 3;
            int expectedX = 3, expectedY = 2, expectedZ = 1;

            PathOperations.SortDescending(ref x, ref y, ref z);

            Assert.AreEqual(expectedX, x);
            Assert.AreEqual(expectedY, y);
            Assert.AreEqual(expectedZ, z);
        }

        [TestMethod]
        public void SortDescending_OnlyFirstSwap_FirstConditionTrue()
        {
            // Путь: x<y=true, x<z=false, y<z=false
            int x = 2, y = 3, z = 1;
            int expectedX = 3, expectedY = 2, expectedZ = 1;

            PathOperations.SortDescending(ref x, ref y, ref z);

            Assert.AreEqual(expectedX, x);
            Assert.AreEqual(expectedY, y);
            Assert.AreEqual(expectedZ, z);
        }

        [TestMethod]
        public void SortDescending_OnlySecondSwap_SecondConditionTrue()
        {
            // Путь: x<y=false, x<z=true, y<z=false
            // Нужно: после обмена x и z, чтобы y >= z
            int x = 2, y = 3, z = 4;
            int expectedX = 4, expectedY = 3, expectedZ = 2;

            PathOperations.SortDescending(ref x, ref y, ref z);

            Assert.AreEqual(expectedX, x);
            Assert.AreEqual(expectedY, y);
            Assert.AreEqual(expectedZ, z);
        }

        [TestMethod]
        public void SortDescending_OnlyThirdSwap_ThirdConditionTrue()
        {
            // Путь: x<y=false, x<z=false, y<z=true
            int x = 3, y = 1, z = 2;
            int expectedX = 3, expectedY = 2, expectedZ = 1;

            PathOperations.SortDescending(ref x, ref y, ref z);

            Assert.AreEqual(expectedX, x);
            Assert.AreEqual(expectedY, y);
            Assert.AreEqual(expectedZ, z);
        }

        // ==================== GCD ====================

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void GCD_NonPositiveNumbers_ThrowsException()
        {
            // Путь: исключение без входа в цикл
            PathOperations.GCD(0, 5);
        }

        [TestMethod]
        public void GCD_EqualNumbers_ReturnsSameNumber()
        {
            // Путь: цикл не выполняется (b=0 сразу)
            int result = PathOperations.GCD(7, 7);
            Assert.AreEqual(7, result);
        }

        [TestMethod]
        public void GCD_OneIteration_SimpleCase()
        {
            // Путь: цикл выполняется 1 раз
            int result = PathOperations.GCD(8, 6);
            Assert.AreEqual(2, result);
        }

        [TestMethod]
        public void GCD_TwoIterations_ComplexCase()
        {
            // Путь: цикл выполняется 2 раза
            int result = PathOperations.GCD(1071, 462); // НОД = 21
            Assert.AreEqual(21, result);
        }

        [TestMethod]
        public void GCD_PrimeNumbers_ReturnsOne()
        {
            // Путь: цикл выполняется несколько раз до b=1
            int result = PathOperations.GCD(17, 13);
            Assert.AreEqual(1, result);
        }

        // ==================== GetEvenDigits ====================

        [TestMethod]
        public void GetEvenDigits_SingleDigit_ReturnsZero()
        {
            // Путь: цикл выполняется 1 раз, позиция нечетная
            int result = PathOperations.GetEvenDigits(5);
            Assert.AreEqual(0, result);
        }

        [TestMethod]
        public void GetEvenDigits_TwoDigits_ReturnsSecondDigit()
        {
            // Путь: цикл выполняется 2 раза
            // 1 итерация: позиция=1 (нечетная) - пропускаем
            // 2 итерация: позиция=2 (четная) - добавляем
            int result = PathOperations.GetEvenDigits(45); // Должно вернуть 4
            Assert.AreEqual(4, result);
        }

        [TestMethod]
        public void GetEvenDigits_FourDigits_ReturnsEvenPositions()
        {
            // Путь: цикл выполняется 4 раза
            // Позиции: 1(пропуск), 2(добавить), 3(пропуск), 4(добавить)
            int result = PathOperations.GetEvenDigits(1234); // Должно вернуть 13
            Assert.AreEqual(13, result);
        }

        [TestMethod]
        public void GetEvenDigits_AllEvenPositionsZero_ReturnsZero()
        {
            // Путь: цикл с добавлением нулей
            int result = PathOperations.GetEvenDigits(1050); // Должно вернуть 00 → 0
            Assert.AreEqual(15, result);
        }

        [TestMethod]
        public void GetEvenDigits_NegativeNumber_AbsoluteValue()
        {
            // Путь: обработка отрицательного числа
            int result = PathOperations.GetEvenDigits(-1234);
            Assert.AreEqual(13, result);
        }

        // ==================== SumOddAboveMainDiagonal ====================

        [TestMethod]
        [ExpectedException(typeof(ArgumentNullException))]
        public void SumOddAboveMainDiagonal_NullArray_ThrowsException()
        {
            // Путь: исключение без циклов
            PathOperations.SumOddAboveMainDiagonal(null);
        }

        [TestMethod]
        public void SumOddAboveMainDiagonal_1x1Array_ReturnsZero()
        {
            // Путь: внешний цикл 1 итерация, внутренний 0 итераций
            int[,] array = { { 5 } };
            int result = PathOperations.SumOddAboveMainDiagonal(array);
            Assert.AreEqual(0, result);
        }

        [TestMethod]
        public void SumOddAboveMainDiagonal_2x2Array_OneOddElement()
        {
            // Путь: проверка условия j>i и нечетности
            int[,] array = {
                { 1, 3 },  // 3 - выше диагонали, нечетное
                { 5, 7 }
            };
            int result = PathOperations.SumOddAboveMainDiagonal(array);
            Assert.AreEqual(3, result);
        }

        [TestMethod]
        public void SumOddAboveMainDiagonal_3x3Array_MultipleOddElements()
        {
            // Путь: множественные итерации с разными условиями
            int[,] array = {
                { 1, 2, 3 },  // 2(четное-пропуск), 3(нечетное-добавить)
                { 4, 5, 6 },  // 6(четное-пропуск)
                { 7, 8, 9 }
            };
            int result = PathOperations.SumOddAboveMainDiagonal(array);
            Assert.AreEqual(3, result); // Только 3
        }

        [TestMethod]
        public void SumOddAboveMainDiagonal_3x3Array_AddMultipleElements()
        {
            // Путь: множественные итерации с разными условиями
            int[,] array = {
                { 1, 5, 3 },  // 5(нечетное-добавить), 3(нечетное-добавить)
                { 4, 5, 6 },  // 6(четное-пропуск)
                { 7, 8, 9 }
            };
            int result = PathOperations.SumOddAboveMainDiagonal(array);
            Assert.AreEqual(8, result); // 3 + 5 = 8
        }

        [TestMethod]
        public void SumOddAboveMainDiagonal_AllEvenElements_ReturnsZero()
        {
            // Путь: все элементы четные - условие нечетности всегда false
            int[,] array = {
                { 2, 4, 6 },
                { 8, 10, 12 },
                { 14, 16, 18 }
            };
            int result = PathOperations.SumOddAboveMainDiagonal(array);
            Assert.AreEqual(0, result);
        }

        [TestMethod]
        public void SumOddAboveMainDiagonal_RectangularArray_ValidResult()
        {
            // Путь: неквадратный массив
            int[,] array = {
                { 1, 3, 5, 7 },  // 3,5,7 - выше диагонали, нечетные
                { 9, 11, 13, 15 } // 13,15 - выше диагонали, нечетные
            };
            int result = PathOperations.SumOddAboveMainDiagonal(array);
            Assert.AreEqual(3 + 5 + 7 + 13 + 15, result);
        }
    }
}