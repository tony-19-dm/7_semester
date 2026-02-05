import pytest
from lab5 import P_digit_number

class TestP_digit_number:
    """Тесты для класса P_digit_number"""
    
    def test_constructor_valid_radix(self):
        """Тест конструктора с допустимыми основаниями"""
        for radix in [2, 8, 10, 16]:
            editor = P_digit_number(radix)
            assert editor.radix == radix
            assert editor.string == "0."
    
    def test_constructor_invalid_radix(self):
        """Тест конструктора с недопустимыми основаниями"""
        with pytest.raises(ValueError):
            P_digit_number(1)
        with pytest.raises(ValueError):
            P_digit_number(17)
    
    def test_is_zero(self):
        """Тест метода is_zero"""
        editor = P_digit_number()
        assert editor.is_zero() == True
        
        editor.string = "5."
        assert editor.is_zero() == False
        
        editor.string = "-0."
        assert editor.is_zero() == True
    
    def test_add_sign(self):
        """Тест метода add_sign"""
        editor = P_digit_number()
        
        # Добавление знака
        result = editor.add_sign()
        assert result == "-0."
        assert editor.string == "-0."
        
        # Удаление знака
        result = editor.add_sign()
        assert result == "0."
        assert editor.string == "0."
    
    def test_add_radix_digit(self):
        """Тест метода add_radix_digit"""
        editor = P_digit_number(10)
        
        # Добавление цифры к нулю
        result = editor.add_radix_digit(5)
        assert result == "5."
        assert editor.string == "5."
        
        # Добавление второй цифры
        result = editor.add_radix_digit(3)
        assert result == "53."
        assert editor.string == "53."
    
    def test_add_radix_digit_hex(self):
        """Тест добавления цифр в шестнадцатеричной системе"""
        editor = P_digit_number(16)
        
        result = editor.add_radix_digit(10)  # A
        assert result == "A."
        assert editor.string == "A."
        
        result = editor.add_radix_digit(15)  # F
        assert result == "AF."
        assert editor.string == "AF."
    
    def test_add_radix_digit_invalid(self):
        """Тест добавления недопустимой цифры"""
        editor = P_digit_number(8)
        
        with pytest.raises(ValueError):
            editor.add_radix_digit(8)
        
        with pytest.raises(ValueError):
            editor.add_radix_digit(9)
    
    def test_add_zero(self):
        """Тест метода add_zero"""
        editor = P_digit_number()
        
        result = editor.add_zero()
        assert result == "0."
        
        editor.string = "5."
        result = editor.add_zero()
        assert result == "50."
    
    def test_backspace(self):
        """Тест метода backspace"""
        editor = P_digit_number()
        editor.string = "123."
        
        result = editor.backspace()
        assert result == "12."
        
        result = editor.backspace()
        assert result == "1."
        
        result = editor.backspace()
        assert result == "0."
    
    def test_backspace_from_zero(self):
        """Тест backspace из нулевого состояния"""
        editor = P_digit_number()
        
        result = editor.backspace()
        assert result == "0."  # Остается нулем
    
    def test_clear(self):
        """Тест метода clear"""
        editor = P_digit_number()
        editor.string = "12345."
        
        result = editor.clear()
        assert result == "0."
        assert editor.string == "0."
    
    def test_edit_commands(self):
        """Тест метода edit с различными командами"""
        editor = P_digit_number(10)
        
        # Команда 0 - очистить
        editor.string = "123."
        result = editor.edit(0)
        assert result == "0."
        
        # Команда 1 - добавить знак
        result = editor.edit(1)
        assert result == "-0."
        
        # Команда 2 - забой символа
        editor.string = "12."
        result = editor.edit(2)
        assert result == "1."
        
        # Команда 3 - добавить ноль
        result = editor.edit(3)
        assert result == "10."
        
        # Команды 4-13 - добавить цифры 0-9
        result = editor.edit(4)  # 0
        assert result == "100."
        
        result = editor.edit(9)  # 5
        assert result == "1005."
    
    def test_edit_invalid_command(self):
        """Тест метода edit с недопустимой командой"""
        editor = P_digit_number(10)
        
        with pytest.raises(ValueError):
            editor.edit(20)
    
    def test_string_property(self):
        """Тест свойств чтения/записи строки"""
        editor = P_digit_number()
        
        # Тест чтения
        assert editor.string == "0."
        
        # Тест записи допустимой строки
        editor.string = "123.45"
        assert editor.string == "123.45"
        
        # Тест записи строки со знаком
        editor.string = "-123.45"
        assert editor.string == "-123.45"
    
    def test_string_property_invalid(self):
        """Тест записи недопустимой строки"""
        editor = P_digit_number(10)
        
        with pytest.raises(ValueError):
            editor.string = "12A.45"  # Недопустимая цифра A для 10-чной системы
        
        with pytest.raises(ValueError):
            editor.string = "12.34.56"  # Много разделителей
    
    def test_binary_system(self):
        """Тест работы с двоичной системой"""
        editor = P_digit_number(2)
        
        assert editor.add_radix_digit(1) == "1."
        assert editor.add_radix_digit(0) == "10."
        
        with pytest.raises(ValueError):
            editor.add_radix_digit(2)
    
    def test_hexadecimal_system(self):
        """Тест работы с шестнадцатеричной системой"""
        editor = P_digit_number(16)
        
        editor.add_radix_digit(10)  # A
        editor.add_radix_digit(11)  # B
        editor.add_radix_digit(12)  # C
        
        assert editor.string == "ABC."
        
        # Проверка допустимости всех цифр
        valid_digits = set("0123456789ABCDEF")
        for i in range(16):
            editor.clear()
            editor.add_radix_digit(i)
            assert editor.string[0] in valid_digits

if __name__ == "__main__":
    pytest.main()