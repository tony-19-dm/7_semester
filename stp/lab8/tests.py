import pytest
from lab8 import TProc, TOprtn, TFunc

class TestTProcInt:
    """Тесты для TProc с целыми числами"""
    
    @pytest.fixture
    def proc(self):
        return TProc(0)
    
    def test_initial_state(self, proc):
        """Тест начального состояния процессора"""
        assert proc.left_operand == 0
        assert proc.right_operand == 0
        assert proc.operation == TOprtn.NONE
    
    def test_basic_operations(self, proc):
        """Тест базовых арифметических операций"""
        test_cases = [
            # (left, right, operation, expected_result)
            (5, 3, TOprtn.ADD, 8),
            (10, 4, TOprtn.SUB, 6),
            (7, 6, TOprtn.MUL, 42),
            (15, 3, TOprtn.DVD, 5),
            (8, 2, TOprtn.ADD, 10),
            (20, 5, TOprtn.SUB, 15),
        ]
        
        for left, right, operation, expected in test_cases:
            proc.left_operand = left
            proc.right_operand = right
            proc.operation = operation
            proc.run_operation()
            assert proc.left_operand == expected
    
    def test_functions(self, proc):
        """Тест математических функций"""
        # Тест квадрата
        proc.right_operand = 5
        proc.run_function(TFunc.SQR)
        assert proc.right_operand == 25
        
        # Тест обратного значения
        proc.right_operand = 4
        proc.run_function(TFunc.REV)
        assert proc.right_operand == 0.25  # 1/4
    
    def test_operation_clear(self, proc):
        """Тест сброса операции"""
        proc.operation = TOprtn.ADD
        proc.reset_operation()
        assert proc.operation == TOprtn.NONE
    
    def test_processor_reset(self, proc):
        """Тест полного сброса процессора"""
        proc.left_operand = 100
        proc.right_operand = 50
        proc.operation = TOprtn.MUL
        proc.reset_processor()
        
        assert proc.left_operand == 0
        assert proc.right_operand == 0
        assert proc.operation == TOprtn.NONE
    
    def test_no_operation_behavior(self, proc):
        """Тест поведения при отсутствии операции"""
        initial_left = proc.left_operand = 10
        proc.right_operand = 5
        # Operation остается NONE
        proc.run_operation()
        assert proc.left_operand == initial_left  # Не должно измениться
    
    def test_operation_set_get(self, proc):
        """Тест установки и получения операции"""
        operations = [TOprtn.ADD, TOprtn.SUB, TOprtn.MUL, TOprtn.DVD, TOprtn.NONE]
        
        for op in operations:
            proc.operation = op
            assert proc.operation == op
    
    def test_operand_set_get(self, proc):
        """Тест установки и получения операндов"""
        proc.left_operand = 123
        proc.right_operand = 456
        
        assert proc.left_operand == 123
        assert proc.right_operand == 456

class Fraction:
    """Простой класс дроби для тестирования"""
    def __init__(self, numerator=0, denominator=1):
        self.numerator = numerator
        self.denominator = denominator
        self._simplify()
    
    def _simplify(self):
        """Упрощение дроби"""
        import math
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        
        gcd = math.gcd(abs(self.numerator), self.denominator)
        if gcd > 1:
            self.numerator //= gcd
            self.denominator //= gcd
    
    def __add__(self, other):
        return Fraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator
        )
    
    def __sub__(self, other):
        return Fraction(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator
        )
    
    def __mul__(self, other):
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )
    
    def __truediv__(self, other):
        return Fraction(
            self.numerator * other.denominator,
            self.denominator * other.numerator
        )
    
    def __eq__(self, other):
        return (self.numerator == other.numerator and 
                self.denominator == other.denominator)
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    
    def rev(self):
        """Обратная дробь"""
        return Fraction(self.denominator, self.numerator)
    
    def sqr(self):
        """Квадрат дроби"""
        return Fraction(self.numerator ** 2, self.denominator ** 2)

class TestTProcFraction:
    """Тесты для TProc с дробями"""
    
    @pytest.fixture
    def proc(self):
        return TProc(Fraction(0, 1))
    
    def test_initial_state_fraction(self, proc):
        """Тест начального состояния с дробями"""
        assert proc.left_operand == Fraction(0, 1)
        assert proc.right_operand == Fraction(0, 1)
        assert proc.operation == TOprtn.NONE
    
    def test_fraction_operations(self, proc):
        """Тест операций с дробями"""
        test_cases = [
            # (left, right, operation, expected_result)
            (Fraction(1, 2), Fraction(1, 3), TOprtn.ADD, Fraction(5, 6)),
            (Fraction(3, 4), Fraction(1, 4), TOprtn.SUB, Fraction(1, 2)),
            (Fraction(2, 3), Fraction(3, 4), TOprtn.MUL, Fraction(1, 2)),
            (Fraction(1, 2), Fraction(2, 3), TOprtn.DVD, Fraction(3, 4)),
        ]
        
        for left, right, operation, expected in test_cases:
            proc.left_operand = left
            proc.right_operand = right
            proc.operation = operation
            proc.run_operation()
            assert proc.left_operand == expected

class TestTProcFloat:
    """Тесты для TProc с числами с плавающей точкой"""
    
    @pytest.fixture
    def proc(self):
        return TProc(0.0)
    
    def test_float_operations(self, proc):
        """Тест операций с числами с плавающей точкой"""
        test_cases = [
            # (left, right, operation, expected_result)
            (2.5, 3.5, TOprtn.ADD, 6.0),
            (10.5, 4.2, TOprtn.SUB, 6.3),
            (2.5, 4.0, TOprtn.MUL, 10.0),
            (15.0, 4.0, TOprtn.DVD, 3.75),
        ]
        
        for left, right, operation, expected in test_cases:
            proc.left_operand = left
            proc.right_operand = right
            proc.operation = operation
            proc.run_operation()
            assert proc.left_operand == pytest.approx(expected)
    
    def test_float_functions(self, proc):
        """Тест функций с числами с плавающей точкой"""
        proc.right_operand = 4.0
        proc.run_function(TFunc.SQR)
        assert proc.right_operand == 16.0
        
        proc.right_operand = 0.25
        proc.run_function(TFunc.REV)
        assert proc.right_operand == 4.0

class TestTProcExceptions:
    """Тесты исключительных ситуаций"""
    
    @pytest.fixture
    def proc(self):
        return TProc(0)
    
    def test_division_by_zero_int(self, proc):
        """Тест деления на ноль для целых чисел"""
        proc.left_operand = 10
        proc.right_operand = 0
        proc.operation = TOprtn.DVD
        
        with pytest.raises(ZeroDivisionError):
            proc.run_operation()
    
    def test_reverse_zero(self, proc):
        """Тест обратного значения для нуля"""
        proc.right_operand = 0
        with pytest.raises(ZeroDivisionError):
            proc.run_function(TFunc.REV)

class TestTProcParametrized:
    """Параметризованные тесты для различных типов данных"""
    
    @pytest.mark.parametrize("left,right,operation,expected", [
        (5, 3, TOprtn.ADD, 8),
        (10, 4, TOprtn.SUB, 6),
        (7, 6, TOprtn.MUL, 42),
        (15, 3, TOprtn.DVD, 5),
    ])
    def test_parametrized_operations_int(self, left, right, operation, expected):
        """Параметризованные тесты операций для целых чисел"""
        proc = TProc(0)
        proc.left_operand = left
        proc.right_operand = right
        proc.operation = operation
        proc.run_operation()
        assert proc.left_operand == expected
    
    @pytest.mark.parametrize("value,function,expected", [
        (5, TFunc.SQR, 25),
        (4, TFunc.SQR, 16),
        (2, TFunc.REV, 0.5),
        (10, TFunc.REV, 0.1),
    ])
    def test_parametrized_functions_int(self, value, function, expected):
        """Параметризованные тесты функций для целых чисел"""
        proc = TProc(0)
        proc.right_operand = value
        proc.run_function(function)
        assert proc.right_operand == expected