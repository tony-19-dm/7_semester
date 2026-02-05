from lab7 import TMemory
import pytest

class TestsMemory:
    def test_initialization(self):
        """Тест инициализации"""
        memory = TMemory[int](0)
        assert memory.Number == 0
        assert memory.State == "Выключена"
        assert memory.ReadMemoryState() == "Выключена"
        assert memory.ReadNumber() == 0

    def test_store(self):
        """Тест записи"""
        memory = TMemory[int](0)

        memory.Store(100)
        assert memory.Number == 100
        assert memory.State == "Включена"

    def test_get(self):
        """Тест получения"""
        memory = TMemory[int](0)
        memory.Store(50)

        result = memory.Get()
        assert result == 50
        assert memory.State == "Включена"

    def test_add(self):
        memory = TMemory[int](0)
        memory.Store(10)
        
        memory.Add(5)
        assert memory.Number == 15
        assert memory.State == "Включена"
    
    def test_clear(self):
        """Тест операции очистки"""
        memory = TMemory[int](0)
        memory.Store(100)
        
        memory.Clear()
        assert memory.Number == 0
        assert memory.State == "Выключена"

    def test_different_types(self):
        """Тест с разными типами данных"""
        
        # Целые числа
        int_memory = TMemory[int](0)
        int_memory.Store(5)
        int_memory.Add(3)
        assert int_memory.Number == 8
        
        # Дробные числа
        float_memory = TMemory[float](0.0)
        float_memory.Store(2.5)
        float_memory.Add(1.5)
        assert float_memory.Number == 4.0
        
        # Строки
        str_memory = TMemory[str]("")
        str_memory.Store("Hello")
        str_memory.Add(" World")
        assert str_memory.Number == "Hello World"
        
        # Списки
        list_memory = TMemory[list]([])
        list_memory.Store([1, 2])
        list_memory.Add([3, 4])
        assert list_memory.Number == [1, 2, 3, 4]

    def test_read_state(self):
        memory = TMemory[int](0)
        assert memory.ReadMemoryState() == "Выключена"

    def test_read_number(self):
        memory = TMemory[int](0)
        memory.Store(40)
        assert memory.ReadNumber() == 40

    def test_default_value(self):
        """Тест что значение по умолчанию сохраняется после очистки"""
        memory = TMemory[int](52)  # Нестандартное значение по умолчанию
        
        memory.Store(777)
        memory.Clear()
        
        assert memory.Number == 52

    def test_properties_consistency(self):
        """Тест согласованности свойств и методов"""
        memory = TMemory[int](0)

        testNum = 69

        testState = "Включена"

        memory.Store(testNum)
        
        assert memory.Number == testNum
        assert memory.ReadNumber() == testNum
        assert memory.Get() == testNum
        
        assert memory.State == testState
        assert memory.ReadMemoryState() == testState

    def test_dict_type_unsupported_add(self):
        """Тест со словарями - сложение не поддерживается"""
        dict_memory = TMemory[dict]({})
        dict_memory.Store({"a": 1})
        
        # Сложение словарей не поддерживается в Python
        with pytest.raises(TypeError):
            dict_memory.Add({"b": 2})

    def test_boolean_type(self):
        """Тест с булевым типом (сложение работает, так как bool наследуется от int)"""
        bool_memory = TMemory[bool](False)
        bool_memory.Store(False)
        assert bool_memory.Number == False
        
        # В Python bool поддерживает сложение (True=1, False=0)
        bool_memory.Add(True)
        assert bool_memory.Number == True