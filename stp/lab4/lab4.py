class Matrix:
    def __init__(self, data):
        if not data or len(data) == 0 or len(data[0]) == 0:
            raise ValueError("Число строк и столбцов должно быть больше 0")
            
        self._data = [row[:] for row in data]  # создаем копию данных
        self._I = len(data)
        self._J = len(data[0])
        
        for row in data:
            if len(row) != self._J:
                raise ValueError("Все строки должны иметь одинаковую длину")
    
    @property
    def I(self):
        return self._I
    
    @property
    def J(self):
        return self._J
    
    def __getitem__(self, indices):
        i, j = indices
        if not (0 <= i < self._I and 0 <= j < self._J):
            raise IndexError(f"Индексы ({i}, {j}) выходят за границы матрицы {self._I}x{self._J}")
        return self._data[i][j]
    
    def __add__(self, other):
        if self._I != other.I or self._J != other.J:
            raise ValueError("Размерности матриц должны совпадать для сложения")
            
        result = [
            [self._data[i][j] + other._data[i][j] for j in range(self._J)]
            for i in range(self._I)
        ]
        return Matrix(result)
    
    def __sub__(self, other):
        if self._I != other.I or self._J != other.J:
            raise ValueError("Размерности матриц должны совпадать для вычитания")
            
        result = [
            [self._data[i][j] - other._data[i][j] for j in range(self._J)]
            for i in range(self._I)
        ]
        return Matrix(result)
    
    def __mul__(self, other):
        if self._J != other.I:
            raise ValueError(f"Матрицы не согласованы для умножения: {self._I}x{self._J} * {other.I}x{other.J}")
            
        result = [[0 for _ in range(other.J)] for _ in range(self._I)]
        
        for i in range(self._I):
            for j in range(other.J):
                for k in range(self._J):
                    result[i][j] += self._data[i][k] * other._data[k][j]
                    
        return Matrix(result)
    
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
            
        if self._I != other.I or self._J != other.J:
            return False
            
        for i in range(self._I):
            for j in range(self._J):
                if self._data[i][j] != other._data[i][j]:
                    return False
        return True
    
    def Transp(self):
        result = [[self._data[j][i] for j in range(self._I)] for i in range(self._J)]
        return Matrix(result)
    
    def Min(self):
        return min(min(row) for row in self._data)
    
    def __str__(self):
        rows = []
        for i in range(self._I):
            row_str = "[" + ", ".join(str(x) for x in self._data[i]) + "]"
            rows.append(row_str)
        return "[" + ", ".join(rows) + "]"
    
    def __repr__(self):
        return f"Matrix({self.__str__()})"