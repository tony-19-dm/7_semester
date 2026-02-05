import pytest
import math
from lab9 import TPoly, TMember

class TestTMember:
    """Тесты для класса TMember (одночлен)"""
    
    def test_constructor(self):
        """Тест конструктора одночлена"""
        # Одночленный полином
        m1 = TMember(6, 3)
        assert m1.coeff == 6
        assert m1.degree == 3
        
        # Константа
        m2 = TMember(3, 0)
        assert m2.coeff == 3
        assert m2.degree == 0
        
        # Нуль-полином
        m3 = TMember()
        assert m3.coeff == 0
        assert m3.degree == 0
        
        # Нуль-полином при нулевом коэффициенте
        m4 = TMember(0, 5)
        assert m4.coeff == 0
        assert m4.degree == 0
    
    def test_equality(self):
        """Тест сравнения одночленов"""
        m1 = TMember(5, 3)
        m2 = TMember(5, 3)
        m3 = TMember(5, 2)
        m4 = TMember(4, 3)
        
        assert m1 == m2
        assert not (m1 == m3)
        assert not (m1 == m4)
        assert not (m3 == m4)
    
    def test_differentiate(self):
        """Тест дифференцирования одночлена"""
        # x^3 -> 3x^2
        m1 = TMember(1, 3)
        deriv1 = m1.differentiate()
        assert deriv1.coeff == 3
        assert deriv1.degree == 2
        
        # 5x^2 -> 10x
        m2 = TMember(5, 2)
        deriv2 = m2.differentiate()
        assert deriv2.coeff == 10
        assert deriv2.degree == 1
        
        # Константа -> 0
        m3 = TMember(7, 0)
        deriv3 = m3.differentiate()
        assert deriv3.coeff == 0
        assert deriv3.degree == 0
        
        # 2x -> 2
        m4 = TMember(2, 1)
        deriv4 = m4.differentiate()
        assert deriv4.coeff == 2
        assert deriv4.degree == 0
    
    def test_evaluate(self):
        """Тест вычисления значения одночлена"""
        m1 = TMember(3, 2)  # 3x^2
        assert abs(m1.evaluate(2) - 12) < 0.0001  # 3*4 = 12
        assert abs(m1.evaluate(0) - 0) < 0.0001
        assert abs(m1.evaluate(-1) - 3) < 0.0001  # 3*1 = 3
        
        m2 = TMember(5, 0)  # 5
        assert abs(m2.evaluate(10) - 5) < 0.0001
        assert abs(m2.evaluate(-5) - 5) < 0.0001
        
        m3 = TMember(-2, 3)  # -2x^3
        assert abs(m3.evaluate(3) + 54) < 0.0001  # -2*27 = -54
    
    def test_to_string(self):
        """Тест строкового представления"""
        assert str(TMember(1, 3)) == "x^3"
        assert str(TMember(-1, 3)) == "-x^3"
        assert str(TMember(5, 3)) == "5x^3"
        assert str(TMember(-5, 3)) == "-5x^3"
        assert str(TMember(1, 1)) == "x"
        assert str(TMember(-1, 1)) == "-x"
        assert str(TMember(7, 0)) == "7"
        assert str(TMember(-7, 0)) == "-7"
        assert str(TMember(0, 5)) == "0"
        assert str(TMember(1, 0)) == "1"
        assert str(TMember(-1, 0)) == "-1"
    
    def test_setters(self):
        """Тест сеттеров"""
        m = TMember(2, 3)
        
        m.coeff = 5
        assert m.coeff == 5
        assert m.degree == 3
        
        m.degree = 4
        assert m.coeff == 5
        assert m.degree == 4
        
        # При установке нулевого коэффициента степень становится 0
        m.coeff = 0
        assert m.coeff == 0
        assert m.degree == 0


class TestTPoly:
    """Тесты для класса TPoly (полином)"""
    
    def test_constructor(self):
        """Тест конструктора полинома"""
        # Одночленный полином
        p1 = TPoly(6, 3)
        assert p1.degree == 3
        assert p1.coeff(3) == 6
        
        # Константа
        p2 = TPoly(3, 0)
        assert p2.degree == 0
        assert p2.coeff(0) == 3
        
        # Нуль-полином
        p3 = TPoly()
        assert p3.degree == 0
        assert p3.is_zero()
        
        # Нуль-полином при нулевом коэффициенте
        p4 = TPoly(0, 5)
        assert p4.degree == 0
        assert p4.is_zero()
    
    def test_degree(self):
        """Тест получения степени полинома"""
        # Создаем полином x^2 + 1
        p1 = TPoly(1, 2)  # x^2
        p1 = p1.add(TPoly(1, 0))  # + 1
        assert p1.degree == 2
        
        p2 = TPoly(17, 0)  # 17
        assert p2.degree == 0
        
        p3 = TPoly()  # 0
        assert p3.degree == 0
    
    def test_coeff(self):
        """Тест получения коэффициента"""
        # Создаем полином x^3 + 2x + 1
        p = TPoly(1, 3)  # x^3
        p = p.add(TPoly(2, 1))  # + 2x
        p = p.add(TPoly(1, 0))  # + 1
        
        assert p.coeff(4) == 0  # Степени 4 нет
        assert p.coeff(3) == 1  # При x^3
        assert p.coeff(1) == 2  # При x
        assert p.coeff(0) == 1  # При константе
        assert p.coeff(2) == 0  # Степени 2 нет
    
    def test_clear(self):
        """Тест очистки полинома"""
        p = TPoly(1, 2)
        p = p.add(TPoly(3, 1))
        assert not p.is_zero()
        
        p.clear()
        assert p.is_zero()
        assert p.degree == 0
    
    def test_addition(self):
        """Тест сложения полиномов"""
        p1 = TPoly(2, 3)  # 2x^3
        p2 = TPoly(3, 2)  # 3x^2
        p3 = TPoly(1, 3)  # x^3
        p4 = TPoly(-1, 3) # -x^3
        
        # 2x^3 + 3x^2
        result1 = p1.add(p2)
        assert result1.coeff(3) == 2
        assert result1.coeff(2) == 3
        
        # 2x^3 + x^3 = 3x^3
        result2 = p1.add(p3)
        assert result2.coeff(3) == 3
        assert result2.degree == 3
        
        # 2x^3 + (-x^3) = x^3
        result3 = p1.add(p4)
        assert result3.coeff(3) == 1
        
        # Сложение с нулевым полиномом
        p_zero = TPoly()
        result4 = p1.add(p_zero)
        assert result4 == p1
    
    def test_multiplication(self):
        """Тест умножения полиномов"""
        # (x + 1) * (x - 1) = x^2 - 1
        p1 = TPoly(1, 1)  # x
        p1 = p1.add(TPoly(1, 0))  # + 1
        
        p2 = TPoly(1, 1)  # x
        p2 = p2.add(TPoly(-1, 0))  # - 1
        
        result = p1.multiply(p2)
        assert result.coeff(2) == 1  # x^2
        assert result.coeff(1) == 0  # x (должен сократиться)
        assert result.coeff(0) == -1  # -1
        
        # Умножение на нулевой полином
        p_zero = TPoly()
        result2 = p1.multiply(p_zero)
        assert result2.is_zero()
        
        # Умножение на константу
        p_const = TPoly(5, 0)  # 5
        result3 = p1.multiply(p_const)  # 5*(x+1) = 5x + 5
        assert result3.coeff(1) == 5
        assert result3.coeff(0) == 5
    
    def test_subtraction(self):
        """Тест вычитания полиномов"""
        p1 = TPoly(2, 3)  # 2x^3
        p2 = TPoly(1, 3)  # x^3
        
        # 2x^3 - x^3 = x^3
        result = p1.subtract(p2)
        assert result.coeff(3) == 1
        
        # x^3 - 2x^3 = -x^3
        result2 = p2.subtract(p1)
        assert result2.coeff(3) == -1
        
        # Вычитание нулевого полинома
        p_zero = TPoly()
        result3 = p1.subtract(p_zero)
        assert result3 == p1
    
    def test_negate(self):
        """Тест унарного минуса"""
        p1 = TPoly(2, 3)  # 2x^3
        p1 = p1.add(TPoly(-1, 1))  # -x
        
        neg = p1.negate()  # -2x^3 + x
        assert neg.coeff(3) == -2
        assert neg.coeff(1) == 1
        assert neg.coeff(0) == 0
        
        # Двойное отрицание должно вернуть исходный полином
        neg2 = neg.negate()
        assert neg2 == p1
    
    def test_equality_poly(self):
        """Тест сравнения полиномов"""
        # x^2 + 2x + 1
        p1 = TPoly(1, 2)  # x^2
        p1 = p1.add(TPoly(2, 1))  # + 2x
        p1 = p1.add(TPoly(1, 0))  # + 1
        
        # Другой полином с такими же коэффициентами
        p2 = TPoly(1, 2)  # x^2
        p2 = p2.add(TPoly(2, 1))  # + 2x
        p2 = p2.add(TPoly(1, 0))  # + 1
        
        # x^2 + 1
        p3 = TPoly(1, 2)  # x^2
        p3 = p3.add(TPoly(1, 0))  # + 1
        
        assert p1 == p2
        assert not (p1 == p3)
        assert not (p2 == p3)
        assert not (p1 == TPoly())
    
    def test_evaluate_poly(self):
        """Тест вычисления значения полинома"""
        # x^2 + 3x
        p = TPoly(1, 2)  # x^2
        p = p.add(TPoly(3, 1))  # + 3x
        
        assert abs(p.evaluate(2) - 10) < 0.0001  # 4 + 6 = 10
        assert abs(p.evaluate(0) - 0) < 0.0001
        assert abs(p.evaluate(-1) + 2) < 0.0001  # 1 - 3 = -2
        
        # Более сложный полином: 2x^3 - x^2 + 4x - 5
        p2 = TPoly(2, 3)    # 2x^3
        p2 = p2.add(TPoly(-1, 2))  # -x^2
        p2 = p2.add(TPoly(4, 1))   # +4x
        p2 = p2.add(TPoly(-5, 0))  # -5
        
        assert abs(p2.evaluate(1) - 0) < 0.0001   # 2 - 1 + 4 - 5 = 0
        assert abs(p2.evaluate(2) - 15) < 0.0001  # 16 - 4 + 8 - 5 = 15
    
    def test_get_member(self):
        """Тест доступа к членам полинома"""
        # x^3 + 2x + 1
        p = TPoly(1, 3)  # x^3
        p = p.add(TPoly(2, 1))  # + 2x
        p = p.add(TPoly(1, 0))  # + 1
        
        # Проверяем члены в порядке убывания степени
        member0 = p.get_member(0)
        assert member0 == (1, 3)  # x^3
        
        member1 = p.get_member(1)
        assert member1 == (2, 1)  # 2x
        
        member2 = p.get_member(2)
        assert member2 == (1, 0)  # 1
        
        # Несуществующий индекс
        assert p.get_member(3) is None
        assert p.get_member(-1) is None
    
    def test_str_representation(self):
        """Тест строкового представления полинома"""
        # Простые полиномы
        assert str(TPoly(1, 2)) == "x^2"
        assert str(TPoly(3, 0)) == "3"
        assert str(TPoly()) == "0"
        
        # x^2 + 2x + 1
        p1 = TPoly(1, 2)  # x^2
        p1 = p1.add(TPoly(2, 1))  # + 2x
        p1 = p1.add(TPoly(1, 0))  # + 1
        assert str(p1) == "x^2 + 2x + 1"
        
        # x^2 - 2x - 1
        p2 = TPoly(1, 2)  # x^2
        p2 = p2.add(TPoly(-2, 1))  # - 2x
        p2 = p2.add(TPoly(-1, 0))  # - 1
        assert str(p2) == "x^2 - 2x - 1"
        
        # 2x^3 - x^2
        p3 = TPoly(2, 3)    # 2x^3
        p3 = p3.add(TPoly(-1, 2))  # - x^2
        assert str(p3) == "2x^3 - x^2"
    
    def test_operator_overloading(self):
        """Тест перегрузки операторов"""
        p1 = TPoly(1, 2)  # x^2
        p2 = TPoly(2, 1)  # 2x
        
        # Сложение
        result_add = p1 + p2
        assert result_add.coeff(2) == 1
        assert result_add.coeff(1) == 2
        
        # Вычитание
        result_sub = p1 - p2
        assert result_sub.coeff(2) == 1
        assert result_sub.coeff(1) == -2
        
        # Умножение
        result_mul = p1 * p2  # x^2 * 2x = 2x^3
        assert result_mul.coeff(3) == 2
        
        # Унарный минус
        result_neg = -p1  # -x^2
        assert result_neg.coeff(2) == -1
    
    def test_normalization(self):
        """Тест нормализации полинома"""
        # Создаем ненормализованный полином: x^2 + 0x + x^2 + (-x^2) + 3
        # Вместо цепочки add, создадим полином напрямую через члены
        poly = TPoly()
        
        # Добавляем члены через внутренний список (для тестирования)
        poly._members.append(TMember(1, 2))   # x^2
        poly._members.append(TMember(0, 1))   # 0x (должен удалиться)
        poly._members.append(TMember(1, 2))   # + x^2 (должен сложиться с первым)
        poly._members.append(TMember(-1, 2))  # + (-x^2) (должен сократиться)
        poly._members.append(TMember(3, 0))   # + 3
        
        # Вызываем нормализацию
        poly._normalize()
        
        # После нормализации должен остаться только 3
        # Все x^2 должны сложиться: 1 + 1 - 1 = 1, но в тесте ожидаем 0
        # Перепишем тест: x^2 + x^2 - x^2 = x^2, плюс константа 3
        assert poly.coeff(2) == 1  # x^2
        assert poly.coeff(1) == 0
        assert poly.coeff(0) == 3
        assert len(poly._members) == 2  # x^2 и 3


def test_complex_polynomial():
    """Тест сложного полинома и операций с ним"""
    # Создаем полином: 3x^4 - 2x^3 + 5x^2 - 7x + 4
    p = TPoly(3, 4)
    p = p.add(TPoly(-2, 3))
    p = p.add(TPoly(5, 2))
    p = p.add(TPoly(-7, 1))
    p = p.add(TPoly(4, 0))
    
    # Проверяем коэффициенты
    assert p.coeff(4) == 3
    assert p.coeff(3) == -2
    assert p.coeff(2) == 5
    assert p.coeff(1) == -7
    assert p.coeff(0) == 4
    
    # Производная: 12x^3 - 6x^2 + 10x - 7
    deriv = p.differentiate()
    print(f"Производная: {deriv}")
    print(f"coeff(3): {deriv.coeff(3)} (ожидается 12)")
    print(f"coeff(2): {deriv.coeff(2)} (ожидается -6)")
    print(f"coeff(1): {deriv.coeff(1)} (ожидается 10)")
    print(f"coeff(0): {deriv.coeff(0)} (ожидается -7)")
    
    assert deriv.coeff(3) == 12
    assert deriv.coeff(2) == -6
    assert deriv.coeff(1) == 10
    assert deriv.coeff(0) == -7
    
    # Вычисление в точке
    assert abs(p.evaluate(1) - 3) < 0.0001  # 3-2+5-7+4 = 3
    assert abs(p.evaluate(0) - 4) < 0.0001
    
    # Умножение на себя (квадрат полинома)
    square = p.multiply(p)
    # Проверяем старшую степень: (3x^4)*(3x^4) = 9x^8
    assert square.degree == 8
    assert square.coeff(8) == 9