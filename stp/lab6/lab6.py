class TEditor:
    """Класс для ввода и редактирования комплексных чисел"""
    
    # Константы
    DECIMAL_SEPARATOR = ","  # разделитель целой и дробной частей
    IMAGINARY_SEPARATOR = "i*"  # разделитель действительной и мнимой частей
    ZERO_REPRESENTATION = "0, i* 0,"  # строковое представление нуля
    
    def __init__(self):
        """Конструктор - инициализирует строку нулевым значением"""
        self._str = self.ZERO_REPRESENTATION
    
    @property
    def _Str_(self):
        """Чтение строки в формате строки (метод свойства)"""
        return self._str
    
    @_Str_.setter
    def _Str_(self, value):
        """Запись строки в формате строки (метод свойства)"""
        if not isinstance(value, str):
            raise ValueError("_Str_ должна быть строкового типа")
        self._str = value
    
    def complexNumberIsZero(self):
        """Проверяет, равно ли комплексное число нулю"""
        try:
            # Более точная проверка - парсим и проверяем числовые значения
            parts = self._parse_complex_string()
            
            # Проверяем, что обе части равны нулю
            real_zero = (parts["real_integer"] == "0" and parts["real_fraction"] == "")
            imag_zero = (parts["imaginary_integer"] == "0" and parts["imaginary_fraction"] == "")
            
            return real_zero and imag_zero
        except:
            return False
    
    def _normalize_string(self, s):
        """Нормализует строку для сравнения"""
        return s.replace(" ", "").lower()
    
    def addSign(self, part="real"):
        """Добавляет или удаляет знак '-' у указанной части"""
        parts = self._parse_complex_string()
        
        if part == "real":
            if parts["real_sign"] == "-":
                parts["real_sign"] = ""
            else:
                parts["real_sign"] = "-"
        elif part == "imaginary":
            if parts["imaginary_sign"] == "-":
                parts["imaginary_sign"] = ""
            else:
                parts["imaginary_sign"] = "-"
        else:
            raise ValueError("Часть должна быть 'real' или 'imaginary'")
        
        self._str = self._build_complex_string(parts)
        return self._str
    
    def addValue(self, digit):
        """Добавляет цифру к строке"""
        if not isinstance(digit, int) or digit < 0 or digit > 9:
            raise ValueError("Цифра должна быть целым числом от 0 до 9")
        
        char_digit = str(digit)
        parts = self._parse_complex_string()
        
        # Определяем, к какой части добавлять цифру
        if self._can_add_to_real(parts):
            if parts["real_integer"] == "0" and parts["real_fraction"] == "":
                parts["real_integer"] = char_digit
            elif parts["real_fraction"] == "":
                parts["real_integer"] += char_digit
            else:
                parts["real_fraction"] += char_digit
        elif self._can_add_to_imaginary(parts):
            if parts["imaginary_integer"] == "0" and parts["imaginary_fraction"] == "":
                parts["imaginary_integer"] = char_digit
            elif parts["imaginary_fraction"] == "":
                parts["imaginary_integer"] += char_digit
            else:
                parts["imaginary_fraction"] += char_digit
        
        self._str = self._build_complex_string(parts)
        return self._str
    
    def addZero(self):
        """Добавляет ноль к строке"""
        return self.addValue(0)
    
    def rmVal(self):
        """Удаляет крайний правый символ"""
        if len(self._str) <= len(self.ZERO_REPRESENTATION):
            # Если _Str_ уже минимальной длины, сбрасываем к нулю
            self.clear()
        else:
            parts = self._parse_complex_string()
            
            # Удаляем символ из соответствующей части
            if parts["imaginary_fraction"] != "":
                parts["imaginary_fraction"] = parts["imaginary_fraction"][:-1]
            elif parts["imaginary_integer"] != "0":
                if len(parts["imaginary_integer"]) > 1:
                    parts["imaginary_integer"] = parts["imaginary_integer"][:-1]
                else:
                    parts["imaginary_integer"] = "0"
            elif parts["real_fraction"] != "":
                parts["real_fraction"] = parts["real_fraction"][:-1]
            elif parts["real_integer"] != "0":
                if len(parts["real_integer"]) > 1:
                    parts["real_integer"] = parts["real_integer"][:-1]
                else:
                    parts["real_integer"] = "0"
            else:
                # Если больше нечего удалять, сбрасываем к нулю
                self.clear()
                return self._str
            
            self._str = self._build_complex_string(parts)
        
        return self._str
    
    def clear(self):
        """Устанавливает нулевое значение комплексного числа"""
        self._str = self.ZERO_REPRESENTATION
        return self._str
    
    def redact(self, command):
        """Выполняет команду редактирования"""
        commands = {
            10: self.clear,
            11: lambda: self.addSign("real"),
            12: self.addZero,
            13: self.rmVal
        }
        
        if command in commands:
            return commands[command]()
        elif command < 10:
            digit = command
            return self.addValue(digit)
        else:
            raise ValueError(f"Неизвестная команда: {command}")
    
    def _parse_complex_string(self):
        """Парсит строку комплексного числа на составляющие части"""
        # Базовая структура для нулевого значения
        parts = {
            "real_sign": "",
            "real_integer": "0",
            "real_fraction": "",
            "imaginary_sign": "", 
            "imaginary_integer": "0",
            "imaginary_fraction": ""
        }
        
        try:
            # Нормализуем строку
            normalized = self._str.replace(" ", "")
            
            # Разделяем действительную и мнимую части
            if self.IMAGINARY_SEPARATOR in normalized:
                real_part, imag_part = normalized.split(self.IMAGINARY_SEPARATOR, 1)
            else:
                real_part = normalized
                imag_part = "0,"
            
            # Парсим действительную часть
            if real_part.startswith("-"):
                parts["real_sign"] = "-"
                real_part = real_part[1:]
            elif real_part.startswith("+"):
                parts["real_sign"] = ""
                real_part = real_part[1:]
            else:
                parts["real_sign"] = ""
            
            if self.DECIMAL_SEPARATOR in real_part:
                real_int, real_frac = real_part.split(self.DECIMAL_SEPARATOR, 1)
                parts["real_integer"] = real_int if real_int else "0"
                parts["real_fraction"] = real_frac
            else:
                # Если нет разделителя, вся часть - целая
                parts["real_integer"] = real_part if real_part else "0"
                parts["real_fraction"] = ""
            
            # Парсим мнимую часть
            if imag_part.startswith("-"):
                parts["imaginary_sign"] = "-"
                imag_part = imag_part[1:]
            elif imag_part.startswith("+"):
                parts["imaginary_sign"] = ""
                imag_part = imag_part[1:]
            else:
                parts["imaginary_sign"] = ""
            
            if self.DECIMAL_SEPARATOR in imag_part:
                imag_int, imag_frac = imag_part.split(self.DECIMAL_SEPARATOR, 1)
                parts["imaginary_integer"] = imag_int if imag_int else "0"
                parts["imaginary_fraction"] = imag_frac
            else:
                # Если нет разделителя, вся часть - целая
                parts["imaginary_integer"] = imag_part if imag_part else "0"
                parts["imaginary_fraction"] = ""
                
        except Exception as e:
            # В случае ошибки парсинга возвращаем нулевое значение
            print(f"Ошибка парсинга: {e}")
            pass
            
        return parts
    
    def _build_complex_string(self, parts):
        """Собирает строку комплексного числа из составляющих частей"""
        # Собираем действительную часть
        real_sign = parts['real_sign']
        real_int = parts['real_integer']
        real_frac = parts['real_fraction']
        
        # Собираем мнимую часть  
        imag_sign = parts['imaginary_sign']
        imag_int = parts['imaginary_integer']
        imag_frac = parts['imaginary_fraction']
        
        # Форматируем строку (без лишних плюсов)
        real_part = f"{real_sign}{real_int}{self.DECIMAL_SEPARATOR}{real_frac}"
        imag_part = f"{imag_sign}{imag_int}{self.DECIMAL_SEPARATOR}{imag_frac}"
        
        # Убираем лишние запятые если дробной части нет
        if not real_frac:
            real_part = real_part.rstrip(self.DECIMAL_SEPARATOR)
        if not imag_frac:
            imag_part = imag_part.rstrip(self.DECIMAL_SEPARATOR)
            
        return f"{real_part} {self.IMAGINARY_SEPARATOR} {imag_part}"
    
    def _can_add_to_real(self, parts):
        """Проверяет, можно ли добавить символ к действительной части"""
        return parts["imaginary_integer"] == "0" and parts["imaginary_fraction"] == ""
    
    def _can_add_to_imaginary(self, parts):
        """Проверяет, можно ли добавить символ к мнимой части"""
        # Можно добавлять к мнимой части, если действительная уже заполнена
        return parts["real_integer"] != "0" or parts["real_fraction"] != ""