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



def exchange_rows(row1, row2, right1, right2):
    for i in range(len(row1)):
        temp = row1[i]
        row1[i] = row2[i]
        row2[i] = temp
    temp = right1
    right1 = right2
    right2 = temp


def add_row(row1, row2):
    new_row = []
    if len(row1) != len(row2):
        raise IndexError("Невозможно провести сложение: ряды разной длины!")
    for i in range(len(row1)):
        new_row = row1[i] + row2[i]
    return new_row

def sub_row(row1, row2):
    new_row = []
    if len(row1) != len(row2):
        raise IndexError("Невозможно провести вычитание: ряды разной длины!")
    for i in range(len(row1)):
        new_row = row1[i] - row2[i]
    return new_row

def mul_row(row, x):
    new_row = []
    for i in range(len(row)):
        new_row = row[i] * x
    return new_row

def div_row(row, x):
    new_row = []
    for i in range(len(row)):
        new_row = row[i] / x
    return new_row

def Jordan_Gauss(left, right):
    col = 0
    row = 0
    main = 0
    step = 0
    for a in range(len(left[0])):
        for i in range(row, len(left)):
            step += 1
            print(f'ШАГ {step}:')
            if(left[i][col] > left[row][col]):
                exchange_rows(left[i], left[row], right[i], right[row])
        main = left[row][col]
        for j in range(len(left[0])):
            left[row][j] /= main
        for r in range(len(left)):
            if(r != row and left[r][col] != Fract(0, 1)):
                left[r] = sub_row(left[r], mul_row(left[row], ((left[r][col])/(left[row][col]))))
        print_matrix(left, right)
        col += 1
                
                    


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