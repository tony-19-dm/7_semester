import pytest
from lab6 import TEditor

class TestTEditorC2:
    
    def test_complex_number_is_zero(self):
        """Тест проверки на нулевое значение"""
        editor = TEditor()
    
        # Тест 1: Начальное значение - ноль
        assert editor.complexNumberIsZero() == True
    
        # Тест 2: После добавления цифры - не ноль
        editor.addValue(1)
        assert editor.complexNumberIsZero() == False
    
        # Тест 3: После очистки - снова ноль
        editor.clear()
        assert editor.complexNumberIsZero() == True
    
        # Тест 4: Различные нулевые представления
        zero_representations = ["0, i* 0,", "0 i* 0", "0 i* 0,"]
        for zero_repr in zero_representations:
            editor._Str_ = zero_repr
            assert editor.complexNumberIsZero() == True
    
    def test_add_sign_real_part(self):
        """Тест изменения знака действительной части"""
        editor = TEditor()
    
        # Тест 1: Смена знака с '' на '-'
        editor._Str_ = "5, i* 3,"
        result = editor.addSign("real")
        assert result == "-5 i* 3"
        
        # Тест 2: Смена знака с '-' на ''
        result = editor.addSign("real")
        assert result == "5 i* 3"
    
    def test_add_sign_imaginary_part(self):
        """Тест изменения знака мнимой части"""
        editor = TEditor()
    
        # Тест 1: Смена знака с '' на '-'
        editor._Str_ = "5, i* 3,"
        result = editor.addSign("imaginary")
        assert result == "5 i* -3"
        
        # Тест 2: Смена знака с '-' на ''
        result = editor.addSign("imaginary")
        assert result == "5 i* 3"
        
        # Тест 3: Неверный параметр
        with pytest.raises(ValueError):
            editor.addSign("invalid_part")
    
    def test_property_setter_validation(self):
        """Тест валидации в сеттере свойства"""
        editor = TEditor()
        
        # Тест 1: Корректные значения
        valid_values = ["1, i* 2,", "3, i* 4,", "0, i* 0,"]
        for value in valid_values:
            editor._Str_ = value
            assert editor._Str_ == value
        
        # Тест 2: Некорректные типы данных
        invalid_values = [123, 45.67, None, [], {}]
        for value in invalid_values:
            with pytest.raises(ValueError):
                editor._Str_ = value

    def test_add_value_validation(self):
        """Тест валидации входных данных addValue"""
        editor = TEditor()
        
        # Тест 1: Корректные цифры
        for digit in range(10):
            result = editor.addValue(digit)
            assert str(digit) in result
        
        # Тест 2: Некорректные цифры
        invalid_digits = [-1, 10, 15, -5, 100]
        for digit in invalid_digits:
            with pytest.raises(ValueError):
                editor.addValue(digit)

    def test_clear_operation(self):
        """Тест операции очистки"""
        editor = TEditor()
        
        # Тест 1: Очистка ненулевого значения
        editor.addValue(5)
        editor.addValue(3)
        assert editor.complexNumberIsZero() == False
        
        result = editor.clear()
        assert result == "0, i* 0,"
        assert editor.complexNumberIsZero() == True

    def test_redact_commands(self):
        """Тест команд редактирования"""
        editor = TEditor()
        
        # Тест 1: Команды цифр (0-9)
        for digit in range(10):
            result = editor.redact(digit)
            assert result is not None
        
        # Тест 2: Специальные команды
        commands = [10, 11, 12, 13]
        
        for cmd in commands:
            result = editor.redact(cmd)
            assert result is not None
        
        # Тест 3: Неверные команды
        invalid_commands = [-1, 14, 15, 100, -5]
        for cmd in invalid_commands:
            with pytest.raises(ValueError):
                editor.redact(cmd)