using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace MathOperations.Tests
{
    [TestClass]
    public class ArrayProcessorC1Tests
    {
        // 1. Поиск минимума из двух чисел

        [TestMethod]
        public void FindMin_FirstLessThanSecond_ReturnsFirst()
        {
            // Ветка: a < b = true
            double a = 2.5, b = 3.7;
            double expected = 2.5;

            double result = ArrayProcessor.FindMin(a, b);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMin_SecondLessThanFirst_ReturnsSecond()
        {
            // Ветка: a < b = false
            double a = 5.2, b = 3.1;
            double expected = 3.1;

            double result = ArrayProcessor.FindMin(a, b);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMin_EqualValues_ReturnsAny()
        {
            // Ветка: a < b = false (при равенстве)
            double a = 4.0, b = 4.0;
            double expected = 4.0;

            double result = ArrayProcessor.FindMin(a, b);

            Assert.AreEqual(expected, result);
        }

        // 2. Поиск максимального значения во всем массиве

        [TestMethod]
        [ExpectedException(typeof(ArgumentNullException))]
        public void FindMaxInArray_NullArray_ThrowsException()
        {
            // Ветка: A == null = true
            double[,] array = null;

            ArrayProcessor.FindMaxInArray(array);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void FindMaxInArray_EmptyArray_ThrowsException()
        {
            // Ветка: A.Length == 0 = true
            double[,] array = new double[0, 0];

            ArrayProcessor.FindMaxInArray(array);
        }

        [TestMethod]
        public void FindMaxInArray_SingleElement_ReturnsElement()
        {
            // Ветки:
            // - Циклы не выполняются (массив 1x1)
            double[,] array = { { 7.5 } };
            double expected = 7.5;

            double result = ArrayProcessor.FindMaxInArray(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxInArray_MaxInFirstElement_ReturnsFirst()
        {
            // Ветка: A[i, j] > max = false для всех элементов кроме первого
            double[,] array = {
                { 10.0, 2.0 },
                { 3.0, 4.0 }
            };
            double expected = 10.0;

            double result = ArrayProcessor.FindMaxInArray(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxInArray_MaxInLastElement_ReturnsLast()
        {
            // Ветка: A[i, j] > max = true для последнего элемента
            double[,] array = {
                { 1.0, 2.0 },
                { 3.0, 15.0 }
            };
            double expected = 15.0;

            double result = ArrayProcessor.FindMaxInArray(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxInArray_MaxInMiddle_ReturnsMiddle()
        {
            // Ветка: A[i, j] > max = true для среднего элемента
            double[,] array = {
                { 1.0, 2.0, 1.0 },
                { 2.0, 20.0, 2.0 },
                { 1.0, 2.0, 1.0 }
            };
            double expected = 20.0;

            double result = ArrayProcessor.FindMaxInArray(array);

            Assert.AreEqual(expected, result);
        }

        // 3. Поиск максимального значения на и выше побочной диагонали

        [TestMethod]
        [ExpectedException(typeof(ArgumentNullException))]
        public void FindMaxAboveSecondaryDiagonal_NullArray_ThrowsException()
        {
            // Ветка: A == null = true
            double[,] array = null;

            ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void FindMaxAboveSecondaryDiagonal_EmptyArray_ThrowsException()
        {
            // Ветка: A.Length == 0 = true
            double[,] array = new double[0, 0];

            ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void FindMaxAboveSecondaryDiagonal_NonSquareArray_ThrowsException()
        {
            // Ветка: rows != cols = true
            double[,] array = new double[2, 3];

            ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);
        }

        [TestMethod]
        public void FindMaxAboveSecondaryDiagonal_1x1Array_ReturnsElement()
        {
            // Ветки:
            // - i + j <= rows - 1 = true (для единственного элемента)
            // - !found = true (первый элемент)
            double[,] array = { { 5.0 } };
            double expected = 5.0;

            double result = ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxAboveSecondaryDiagonal_MaxOnDiagonal_ReturnsDiagonalElement()
        {
            // Ветка: i + j <= rows - 1 = true для элементов выше диагонали
            // Максимум находится на самой диагонали
            double[,] array = {
                { 1.0, 2.0, 3.0 },
                { 4.0, 5.0, 6.0 },
                { 7.0, 8.0, 9.0 }
            };
            double expected = 7.0; // Элемент на побочной диагонали

            double result = ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxAboveSecondaryDiagonal_MaxAboveDiagonal_ReturnsAboveElement()
        {
            // Ветка: i + j <= rows - 1 = true для элементов выше диагонали
            // Максимум находится выше диагонали
            double[,] array = {
                { 1.0, 15.0, 2.0 },  // 15.0 - выше диагонали
                { 4.0, 5.0, 6.0 },
                { 7.0, 8.0, 9.0 }
            };
            double expected = 15.0;

            double result = ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        [ExpectedException(typeof(ArgumentException))]
        public void FindMaxAboveSecondaryDiagonal_NonSquareArrayThrowsException()
        {
            // Ветка: Массив должен быть квадратным
            double[,] array = {
                { 1.0, 2.0, 3.0 },
                { 4.0, 5.0, 6.0 }
            }; 

            ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

        }

        [TestMethod]
        public void FindMaxAboveSecondaryDiagonal_NegativeValues_WorksCorrectly()
        {
            // Ветка: проверка работы с отрицательными числами
            double[,] array = {
                { -5.0, -2.0 },
                { -3.0, -1.0 }
            };
            double expected = -2.0; // Максимум среди отрицательных

            double result = ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxAboveSecondaryDiagonal_MaxChangesMultipleTimes_CorrectResult()
        {
            // Ветка: A[i, j] > max = true несколько раз в цикле
            double[,] array = {
                { 1.0, 10.0, 3.0 },   // 10.0 становится максимумом
                { 4.0, 15.0, 5.0 },
                { 7.0, 8.0, 9.0 }
            };
            double expected = 15.0;

            double result = ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

            Assert.AreEqual(expected, result);
        }

        [TestMethod]
        public void FindMaxAboveSecondaryDiagonal_FirstElementIsMax_ReturnsFirst()
        {
            // Ветка: !found = true (первый элемент), затем A[i, j] > max = false для остальных
            double[,] array = {
                { 100.0, 2.0, 3.0 },
                { 4.0, 5.0, 6.0 },
                { 7.0, 8.0, 9.0 }
            };
            double expected = 100.0;

            double result = ArrayProcessor.FindMaxAboveSecondaryDiagonal(array);

            Assert.AreEqual(expected, result);
        }
    }
}