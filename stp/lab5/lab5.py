class P_digit_number:

    DECIMAL_SEPARATOR = '.'
    ZERO_REPRESENTATION = '0.'

    def __init__(self, radix = 10):

        if (radix < 2 or radix > 16):
            raise ValueError("Основание системы счисления должно быть от 2 до 16")
        
        self._radix = radix
        self._string = self.ZERO_REPRESENTATION

    @property
    def radix(self):
        return self._radix
    
    @property
    def string(self):
        return self._string
    
    @string.setter
    def string(self, value):
        if not self._is_valid_string(value):
            raise ValueError("Недопустимый формат строки")
        self._string = value
    
    def _is_valid_string(self, s):
        if not s:
            return False
        
        if s.count(self.DECIMAL_SEPARATOR) > 1:
            return False
        
        parts = s.split(self.DECIMAL_SEPARATOR)
        integer_part = parts[0]
        fractional_part = parts[1] if len(parts) > 1 else ""
        
        if integer_part.startswith('-'):
            integer_part = integer_part[1:]
        
        valid_digits = self._get_valid_digits()
        
        for char in integer_part + fractional_part:
            if char not in valid_digits:
                return False
        
        return True
    
    def _get_valid_digits(self):
        digits = "0123456789ABCDEF"
        return set(digits[:self._radix])
    
    def is_zero(self):
        # Убираем знак и проверяем, равно ли число нулю
        clean_string = self._string.lstrip('-')
        return clean_string == self.ZERO_REPRESENTATION
    
    def add_sign(self):
        if self._string.startswith('-'):
            self._string = self._string[1:]
        else:
            self._string = '-' + self._string
        return self._string
    
    def add_radix_digit(self, digit):
        if not 0 <= digit < self._radix:
            raise ValueError(f"Цифра {digit} недопустима для системы счисления с основанием {self._radix}")
        
        digits = "0123456789ABCDEF"
        char = digits[digit]
        
        if self.is_zero():
            self._string = char + self.DECIMAL_SEPARATOR
        else:
            if self.DECIMAL_SEPARATOR in self._string:
                parts = self._string.split(self.DECIMAL_SEPARATOR)
                integer_part = parts[0]
                fractional_part = parts[1]
                self._string = integer_part + char + self.DECIMAL_SEPARATOR + fractional_part
            else:
                self._string += char
        
        return self._string
    
    def add_zero(self):
        return self.add_radix_digit(0)
    
    def backspace(self):
        if self.is_zero():
            return self._string
        
        # Разделяем на целую и дробную части
        if self.DECIMAL_SEPARATOR in self._string:
            parts = self._string.split(self.DECIMAL_SEPARATOR)
            integer_part = parts[0]
            fractional_part = parts[1] if len(parts) > 1 else ""
            
            # Если есть цифры в целой части (кроме возможного знака)
            if len(integer_part) > 1 or (len(integer_part) == 1 and not integer_part.startswith('-')):
                # Удаляем последний символ из целой части
                new_integer_part = integer_part[:-1]
                
                # Если после удаления целая часть пустая или содержит только знак
                if new_integer_part == '' or new_integer_part == '-':
                    self._string = self.ZERO_REPRESENTATION
                else:
                    self._string = new_integer_part + self.DECIMAL_SEPARATOR + fractional_part
            else:
                # Если в целой части только одна цифра (или знак), устанавливаем ноль
                self._string = self.ZERO_REPRESENTATION
        else:
            # Если нет разделителя (не должно происходить в нормальном состоянии)
            if len(self._string) > 1:
                self._string = self._string[:-1]
            else:
                self._string = self.ZERO_REPRESENTATION
        
        return self._string
    
    def clear(self):
        self._string = self.ZERO_REPRESENTATION
        return self._string
    
    def edit(self, command):
        if command == 0:
            return self.clear()
        elif command == 1:
            return self.add_sign()
        elif command == 2:
            return self.backspace()
        elif command == 3:
            return self.add_zero()
        elif 4 <= command < 4 + self._radix:
            digit = command - 4
            return self.add_radix_digit(digit)
        else:
            raise ValueError(f"Неизвестная команда: {command}")
