import math
from typing import TypeVar, Generic, Iterator

class TFrac:
    """Класс для представления простой дроби"""
    
    def __init__(self, numerator=0, denominator=1):
        """Конструктор дроби"""
        if denominator == 0:
            raise ValueError("Знаменатель не может быть равен 0")
        
        self.numerator = numerator
        self.denominator = denominator
        self._normalize()
    
    def _normalize(self):
        """Приведение дроби к нормальной форме"""
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        
        gcd_val = math.gcd(abs(self.numerator), self.denominator)
        if gcd_val > 1:
            self.numerator //= gcd_val
            self.denominator //= gcd_val
    
    def __eq__(self, other):
        """Проверка равенства дробей"""
        if isinstance(other, TFrac):
            return (self.numerator == other.numerator and 
                   self.denominator == other.denominator)
        return False
    
    def __hash__(self):
        """Хэш для использования в множестве"""
        return hash((self.numerator, self.denominator))
    
    def __str__(self):
        """Строковое представление дроби"""
        return f"{self.numerator}/{self.denominator}"
    
    def __repr__(self):
        """Представление для отладки"""
        return f"TFrac({self.numerator}, {self.denominator})"
    
    def copy(self):
        """Создание копии дроби"""
        return TFrac(self.numerator, self.denominator)

T = TypeVar('T')


class tset(Generic[T]):
    """Шаблон класса множество"""
    
    def __init__(self):
        """Конструктор - создает пустое множество"""
        self._data = set()
    
    def clear(self) -> None:
        """Опустошить множество"""
        self._data.clear()
    
    def add(self, d: T) -> None:
        """Добавить элемент в множество"""
        self._data.add(d)
    
    def remove(self, d: T) -> None:
        """Удалить элемент из множества"""
        if d in self._data:
            self._data.remove(d)
        else:
            raise KeyError(f"Элемент {d} не найден в множестве")
    
    def is_empty(self) -> bool:
        """Проверить, пусто ли множество"""
        return not self._data
    
    def contains(self, d: T) -> bool:
        """Проверить, принадлежит ли элемент множеству"""
        return d in self._data
    
    def union(self, q: 'tset[T]') -> 'tset[T]':
        """Объединить множества (сложение)"""
        result = tset[T]()
        result._data = self._data.union(q._data)
        return result
    
    def difference(self, q: 'tset[T]') -> 'tset[T]':
        """Вычесть множество"""
        result = tset[T]()
        result._data = self._data.difference(q._data)
        return result
    
    def intersection(self, q: 'tset[T]') -> 'tset[T]':
        """Пересечение множеств (умножение)"""
        result = tset[T]()
        result._data = self._data.intersection(q._data)
        return result
    
    def size(self) -> int:
        """Количество элементов во множестве"""
        return len(self._data)
    
    def get_element(self, j: int) -> T:
        """Получить элемент по индексу (для перебора)"""
        if j < 1 or j > self.size():
            raise IndexError(f"Индекс {j} вне диапазона [1, {self.size()}]")
        
        # Преобразуем множество в список для доступа по индексу
        return list(self._data)[j - 1]
    
    def __str__(self) -> str:
        """Строковое представление множества"""
        elements = list(self._data)
        return "{" + ", ".join(str(e) for e in elements) + "}"
    
    def __eq__(self, other: object) -> bool:
        """Проверка равенства множеств"""
        if not isinstance(other, tset):
            return False
        return self._data == other._data
    
    def __iter__(self) -> Iterator[T]:
        """Итератор по элементам множества"""
        return iter(self._data)
    
    def copy(self) -> 'tset[T]':
        """Создать копию множества"""
        result = tset[T]()
        result._data = self._data.copy()
        return result