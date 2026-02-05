from enum import Enum
from typing import TypeVar, Generic

T = TypeVar('T')

class TOprtn(Enum):
    NONE = 0
    ADD = 1
    SUB = 2
    MUL = 3
    DVD = 4

class TFunc(Enum):
    REV = 1
    SQR = 2

class TProc(Generic[T]):
    def __init__(self, default_value: T):
        self._lop_res = default_value
        self._rop = default_value
        self._operation = TOprtn.NONE

    def reset_processor(self) -> None:
        """Сброс процессора в начальное состояние"""
        self._lop_res = self._get_default_value()
        self._rop = self._get_default_value()
        self._operation = TOprtn.NONE

    def reset_operation(self) -> None:
        """Сброс текущей операции"""
        self._operation = TOprtn.NONE

    def run_operation(self) -> None:
        """Выполнение текущей операции"""
        if self._operation == TOprtn.NONE:
            return

        op_map = {
            TOprtn.ADD: lambda x, y: x + y,
            TOprtn.SUB: lambda x, y: x - y,
            TOprtn.MUL: lambda x, y: x * y,
            TOprtn.DVD: lambda x, y: x / y,
        }
        self._lop_res = op_map[self._operation](self._lop_res, self._rop)

    def run_function(self, func: TFunc) -> None:
        """Выполнение функции над правым операндом"""
        func_map = {
            TFunc.REV: lambda x: 1 / x,
            TFunc.SQR: lambda x: x * x,
        }
        self._rop = func_map[func](self._rop)

    @property
    def left_operand(self) -> T:
        return self._lop_res

    @left_operand.setter
    def left_operand(self, value: T) -> None:
        self._lop_res = value

    @property
    def right_operand(self) -> T:
        return self._rop

    @right_operand.setter
    def right_operand(self, value: T) -> None:
        self._rop = value

    @property
    def operation(self) -> TOprtn:
        return self._operation

    @operation.setter
    def operation(self, value: TOprtn) -> None:
        self._operation = value

    def _get_default_value(self) -> T:
        return type(self._lop_res)()