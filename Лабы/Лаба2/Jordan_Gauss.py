import math

class Fract:
    def __init__(self, upper, lower):
        if lower == 0:
            raise ValueError("Знаменатель не может быть 0!")
        if lower < 0:
            upper = -upper
            lower = -lower
        self.upper = upper
        self.lower = lower
        self.reduce()

    def __print__(self):
        if self.upper % self.lower == 0:
            print(self.upper // self.lower)
        else:
            print(f'({self.upper}/{self.lower})')

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

        left_part = list(map(int, left.strip().split()))
        right_part = int(right.strip())

        left_matrix.append(left_part)
        right_vector.append(right_part)
    return left_matrix, right_vector

def print_matrix(left, right):
    for i in range(len(left)):
        print(*[f"{x:6d}" for x in left[i]], f" | {right[i]:6d}")

if __name__ == "__main__":
    path = ".\Лабы\Лаба2\matrix"
    print(80 * "-")
    print( (20 * " ") + "Лабораторная работа №2" + (20 * " "))
    print( (20 * " ") + "МЕТОД ЖОРДАНА-ГАУССА" + (20 * " "))
    print(80 * "-")
    print("\nInput filename of matrix: ")
    name = input()
    if not name.__contains__(".txt"):
        name = name + ".txt"
    f_matrix = open(f'{path}\{name}', "r")
    s_matrix = f_matrix.read()
    f_matrix.close()

    
    m_left, m_right = parse_matrix(s_matrix)
    
    print("Исходная матрица:")
    print_matrix(m_left, m_right)