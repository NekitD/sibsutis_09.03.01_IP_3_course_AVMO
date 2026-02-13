import math

class Fract:
    def __init__(self, upper, lower=1):
        if lower == 0:
            raise ValueError("Знаменатель не может быть 0!")
        if lower < 0:
            upper = -upper
            lower = -lower
        self.upper = upper
        self.lower = lower
        self.reduce()

    def __str__(self):
        if self.upper % self.lower == 0:
            return str(self.upper // self.lower)
        else:
            return f'({self.upper}/{self.lower})'

    def reduce(self):
        gcd = math.gcd(self.upper, self.lower)
        self.upper //= gcd
        self.lower //= gcd

    def __mul__(self, x):
        if isinstance(x, Fract):
            return Fract(self.upper * x.upper, self.lower * x.lower)
        elif isinstance(x, (int, float)):
            return Fract(self.upper * x, self.lower)
        else:
            raise TypeError("Ошибка умножения дроби!")

    def __truediv__(self, x):
        if isinstance(x, Fract):
            return Fract(self.upper * x.lower, self.lower * x.upper)
        elif isinstance(x, (int, float)):
            return Fract(self.upper, self.lower * x)
        else:
            raise TypeError("Ошибка деления дроби!")

    def __add__(self, x):
        if isinstance(x, Fract):
            new_upper = self.upper * x.lower + x.upper * self.lower
            new_lower = self.lower * x.lower
            return Fract(new_upper, new_lower)
        elif isinstance(x, (int, float)):
            return Fract(self.upper + x * self.lower, self.lower)
        else:
            raise TypeError("Ошибка сложения дробей!")

    def __sub__(self, x):
        if isinstance(x, Fract):
            new_upper = self.upper * x.lower - x.upper * self.lower
            new_lower = self.lower * x.lower
            return Fract(new_upper, new_lower)
        elif isinstance(x, (int, float)):
            return Fract(self.upper - x * self.lower, self.lower)
        else:
            raise TypeError("Ошибка вычитания из дроби!")
    
    def __eq__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower == x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper == x * self.lower
        return False

    def __ne__(self, x):
        return not self.__eq__(x)

    def __gt__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower > x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper > x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __ge__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower >= x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper >= x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __lt__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower < x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper < x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __le__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower <= x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper <= x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __abs__(self):
        return Fract(abs(self.upper), self.lower)

def parse_matrix(matrix_str):
    rows = matrix_str.strip().split('\n')
    left_matrix = []  
    right_vector = []   
    for row in rows:
        left, right = row.strip().split('|')
        left_parts = left.strip().split()
        left_part = []
        for num in left_parts:
            if '/' in num:
                up, low = map(int, num.split('/'))
                left_part.append(Fract(up, low))
            else:
                left_part.append(Fract(int(num)))
        right_str = right.strip()
        if '/' in right_str:
            up, low = map(int, right_str.split('/'))
            right_part = Fract(up, low)
        else:
            right_part = Fract(int(right_str))
        
        left_matrix.append(left_part)
        right_vector.append(right_part)
    
    return left_matrix, right_vector

def print_matrix(left_matrix, right_vector):
    for i in range(len(left_matrix)):
        row_str = ""
        for j in range(len(left_matrix[i])):
            row_str += f"{str(left_matrix[i][j]):>8} "
        row_str += f"| {str(right_vector[i]):>8}"
        print(row_str)


def Jordan_Gauss(left, right):
    n = len(left)
    m = len(left[0])

    option = 0
    
    for col in range(min(n, m)):
        print('-' * 50)
        print(f'ШАГ {col + 1}:')
        main_row = col
        for i in range(col, n):
            if abs(left[i][col]) > abs(left[main_row][col]):
                main_row = i
        
        if main_row != col:
            left[col], left[main_row] = left[main_row], left[col]
            right[col], right[main_row] = right[main_row], right[col]
            print(f'Меняем строки {main_row} и {col} местами:')
            print_matrix(left, right)
        
        main = left[col][col]
        print(f'Главный элемент ({col},{col}): {main}')
        for j in range(col, m):
            left[col][j] = left[col][j] / main
        right[col] = right[col] / main
        print(f'Делим {main_row} строку на {main}:')
        print_matrix(left, right)
        
        for i in range(n):
            if i != col:
                d = left[i][col]
                if d.upper != 0:
                    for j in range(col, m):
                        left[i][j] = left[i][j] - (left[col][j] * d)
                    right[i] = right[i] - (right[col] * d)
        print(f'Зануляем элементы над и под 1 в столбце {col}:')
        print_matrix(left, right)
        print()
    if(option == 0):
        print("Система имеет единственное решение:")
        for i in range(len(left)):
            print(f'x{i+1} = {right[i]}')
    elif (option == 1):
        print("Система имеет бесконечное множество решений.")
        print("Общий вид:")
        row = 0
        col = 0
        for col, row in range(m):
            dec = f'x{i+1} = '
            sign = False
            if(right[row] != Fract(0, 1)):
                dec += f'({right[row]})'
                sign = True
            for s in range(m):
                if(s != col and left[row][s] != Fract(0, 1)):
                    if(sign):
                        dec += f' + ({left[row][s] * (-1)})'
                    else:
                        dec += f'({left[row][s] * (-1)})'
            print(dec)
    else:
        print("Система не имеет решений!")

if __name__ == "__main__":
    path = ".\Лабы\Лаба2\matrix"
    print(80 * "-")
    print( (20 * " ") + "Лабораторная работа №2" + (20 * " "))
    print( (20 * " ") + "МЕТОД ЖОРДАНА-ГАУССА" + (20 * " "))
    print(80 * "-")
    while(1):
        print("\nInput filename of matrix (or exit to shutdown the program): ")
        name = input()
    
        if (name == "exit"):
            print("Shutting Down")
            break
    
        if not name.__contains__(".txt"):
            name = name + ".txt"
        f_matrix = open(f'{path}\{name}', "r")
        s_matrix = f_matrix.read()
        f_matrix.close()

        m_left, m_right = parse_matrix(s_matrix)
    
        print("Исходная матрица:")
        print_matrix(m_left, m_right)

        Jordan_Gauss(m_left, m_right)