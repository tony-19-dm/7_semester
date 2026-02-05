from typing import TypeVar, Generic, Callable

T = TypeVar('T')

class TMemory(Generic[T]):

    _On = "Включена"
    _Off = "Выключена"

    def __init__(self, default_value: T):

        self._default_value = default_value  # Значение по умолчанию типа T
        self._FNumber = default_value        # Текущее значение типа T
        self._FState = self._Off

    def Store(self, value: T) -> None:
        self._FNumber = value
        self._FState = self._On

    def Get(self) -> T:
        self._FState = self._On
        return self._FNumber

    def Add(self, value: T):
        try:
            self._FNumber = self._FNumber + value
            self._FState = self._On
        except TypeError as e:
            raise TypeError(f"Тип {type(self._FNumber).__name__} не поддерживает операцию сложения") from e
        
    def Clear(self) -> None:
        self._FNumber = self._default_value
        self._FState = self._Off

    def ReadMemoryState(self) -> str:
        return self._FState
    
    def ReadNumber(self) -> T:
        return self._FNumber
    
    @property
    def Number(self) -> T:
        return self._FNumber
    
    @property
    def State(self) -> str:
        return self._FState