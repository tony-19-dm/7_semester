from typing import List, Tuple, Optional
from collections import defaultdict
import math

class TMember:
    """Класс для представления одночлена (члена полинома)"""
    
    def __init__(self, coeff: int = 0, degree: int = 0):
        """
        Конструктор одночлена
        Args:
            coeff: коэффициент одночлена
            degree: степень одночлена
        """
        self._coeff = coeff
        self._degree = degree if coeff != 0 else 0
    
    @property
    def coeff(self) -> int:
        """Чтение коэффициента"""
        return self._coeff
    
    @property
    def degree(self) -> int:
        """Чтение степени"""
        return self._degree
    
    @coeff.setter
    def coeff(self, value: int) -> None:
        """Запись коэффициента"""
        self._coeff = value
        if value == 0:
            self._degree = 0
    
    @degree.setter
    def degree(self, value: int) -> None:
        """Запись степени"""
        self._degree = value
        if self._coeff == 0:
            self._degree = 0
    
    def __eq__(self, other: object) -> bool:
        """Сравнение одночленов на равенство"""
        if not isinstance(other, TMember):
            return False
        return self._coeff == other._coeff and self._degree == other._degree
    
    def differentiate(self) -> 'TMember':
        """Вычисление производной одночлена"""
        if self._degree == 0:
            return TMember(0, 0)
        return TMember(self._coeff * self._degree, self._degree - 1)
    
    def evaluate(self, x: float) -> float:
        """Вычисление значения одночлена в точке x"""
        if self._degree == 0:
            return float(self._coeff)
        return float(self._coeff) * (x ** self._degree)
    
    def to_string(self) -> str:
        """Строковое представление одночлена"""
        if self._coeff == 0:
            return "0"
        
        result = ""
        
        # Коэффициент
        if self._coeff != 1 and self._coeff != -1:
            result += str(self._coeff)
        elif self._coeff == -1:
            result += "-"
        
        # Переменная x
        if self._degree > 0:
            result += "x"
            if self._degree > 1:
                result += f"^{self._degree}"
        
        # Если степень 0, а коэффициент не отобразился
        if self._degree == 0 and (self._coeff == 1 or self._coeff == -1):
            result += str(abs(self._coeff))
        
        return result
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"TMember(coeff={self._coeff}, degree={self._degree})"
    
    def is_zero(self) -> bool:
        """Проверка, является ли одночлен нулевым"""
        return self._coeff == 0


class TPoly:
    """Класс для представления полинома с целыми коэффициентами"""
    
    def __init__(self, coeff: int = 0, degree: int = 0):
        """
        Конструктор полинома
        Args:
            coeff: коэффициент для одночленного полинома
            degree: степень для одночленного полинома
        """
        self._members: List[TMember] = []
        if coeff != 0:
            self._members.append(TMember(coeff, degree))
        self._normalize()
    
    def _normalize(self) -> None:
        """Нормализация полинома: сортировка по убыванию степени и удаление нулевых членов"""
        if not self._members:
            return
        
        # Объединение членов с одинаковой степенью
        coeff_dict = defaultdict(int)
        for member in self._members:
            if member.coeff != 0:
                coeff_dict[member.degree] += member.coeff
        
        # Создание нового списка членов
        self._members = []
        for degree in sorted(coeff_dict.keys(), reverse=True):
            coeff = coeff_dict[degree]
            if coeff != 0:
                self._members.append(TMember(coeff, degree))
    
    def _copy(self) -> 'TPoly':
        """Создание копии полинома"""
        new_poly = TPoly()
        new_poly._members = [TMember(m.coeff, m.degree) for m in self._members]
        return new_poly
    
    @property
    def degree(self) -> int:
        """Степень полинома"""
        if not self._members:
            return 0
        return self._members[0].degree
    
    def coeff(self, n: int) -> int:
        """
        Коэффициент при степени n
        Args:
            n: степень
        Returns:
            Коэффициент при x^n или 0, если такой степени нет
        """
        for member in self._members:
            if member.degree == n:
                return member.coeff
        return 0
    
    def clear(self) -> None:
        """Очистка полинома (превращение в нуль-полином)"""
        self._members = []
    
    def add(self, other: 'TPoly') -> 'TPoly':
        """Сложение полиномов"""
        result = self._copy()
        
        # Добавляем члены второго полинома
        for member in other._members:
            result._members.append(TMember(member.coeff, member.degree))
        
        result._normalize()
        return result
    
    def multiply(self, other: 'TPoly') -> 'TPoly':
        """Умножение полиномов"""
        result = TPoly()
        
        # Перемножаем каждый член первого полинома с каждым членом второго
        for m1 in self._members:
            for m2 in other._members:
                new_coeff = m1.coeff * m2.coeff
                new_degree = m1.degree + m2.degree
                result._members.append(TMember(new_coeff, new_degree))
        
        result._normalize()
        return result
    
    def subtract(self, other: 'TPoly') -> 'TPoly':
        """Вычитание полиномов"""
        result = self._copy()
        
        # Добавляем члены второго полинома с обратными знаками
        for member in other._members:
            result._members.append(TMember(-member.coeff, member.degree))
        
        result._normalize()
        return result
    
    def negate(self) -> 'TPoly':
        """Унарный минус (противоположный полином)"""
        result = TPoly()
        result._members = [TMember(-member.coeff, member.degree) for member in self._members]
        result._normalize()
        return result
    
    def __eq__(self, other: object) -> bool:
        """Сравнение полиномов на равенство"""
        if not isinstance(other, TPoly):
            return False
        
        if len(self._members) != len(other._members):
            return False
        
        for m1, m2 in zip(self._members, other._members):
            if m1.coeff != m2.coeff or m1.degree != m2.degree:
                return False
        
        return True
    
    def differentiate(self) -> 'TPoly':
        """Дифференцирование полинома"""
        result = TPoly()
        
        for member in self._members:
            if member.degree > 0:
                deriv = member.differentiate()
                if deriv.coeff != 0:
                    result._members.append(deriv)
        
        result._normalize()
        return result
    
    def evaluate(self, x: float) -> float:
        """Вычисление значения полинома в точке x"""
        result = 0.0
        for member in self._members:
            result += member.evaluate(x)
        return result
    
    def get_member(self, i: int) -> Optional[Tuple[int, int]]:
        """
        Доступ к i-му члену полинома
        Args:
            i: индекс члена (начиная с 0)
        Returns:
            Кортеж (коэффициент, степень) или None, если индекс вне диапазона
        """
        if 0 <= i < len(self._members):
            member = self._members[i]
            return (member.coeff, member.degree)
        return None
    
    def __str__(self) -> str:
        """Строковое представление полинома"""
        if not self._members:
            return "0"
        
        terms = []
        for member in self._members:
            term_str = member.to_string()
            terms.append(term_str)
        
        # Собираем все члены в строку
        result = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                result += f" - {term[1:]}"
            else:
                result += f" + {term}"
        
        return result
    
    def __repr__(self) -> str:
        return f"TPoly({str(self)})"
    
    def is_zero(self) -> bool:
        """Проверка, является ли полином нулевым"""
        return len(self._members) == 0
    
    def to_polynomial_string(self) -> str:
        """Альтернативное строковое представление полинома"""
        return str(self)
    
    def __add__(self, other: 'TPoly') -> 'TPoly':
        """Перегрузка оператора +"""
        return self.add(other)
    
    def __sub__(self, other: 'TPoly') -> 'TPoly':
        """Перегрузка оператора -"""
        return self.subtract(other)
    
    def __mul__(self, other: 'TPoly') -> 'TPoly':
        """Перегрузка оператора *"""
        return self.multiply(other)
    
    def __neg__(self) -> 'TPoly':
        """Перегрузка унарного минуса"""
        return self.negate()