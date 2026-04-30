import math
from itertools import combinations
from Fract import Fract
from MatrixFunctions import parse_matrix


def isBasic(x, y, matrix):
    for i in range(len(matrix)):
        if ((i != x) and (matrix[i][y]) != 0):
            return False
    return True

def mulRowVal(row, val):
    for i in range(len(row)):
        row[i] *= val

def divRowVal(row, val):
    for i in range(len(row)):
        row[i] /= val

def printTable(matrix, basis, b_vector, z_vector, z, co_vector, rr, rc):
    col_width = 12
    def center(text, width=col_width):
        text = str(text)
        if len(text) > width:
            return text[:width-3] + "..."
        return text.center(width)
    
    border = "+" + "-" * col_width + "+" + "-" * col_width + "+"
    
    for _ in range(len(matrix[0])):
        border += "-" * col_width + "+"
    print(border.replace("-", "="))
    
    header = "|" + center("Б.п") + "|" + center("1") + "|"
    for i in range(len(matrix[0])):
        header += center(f"x{i+1}") + "|"
    print(header)
    print(border.replace("-", "="))
    

    for x in range(len(basis)):
        row = "|" + center(f"x{basis[x]+1}") + "|" + center(str(b_vector[x])) + "|"
        for y in range(len(matrix[x])):
            if x == rr and y == rc: 
                row += center(f'[{matrix[x][y]}]') + "|"
            else:
                row += center(str(matrix[x][y])) + "|"
        print(row)
        print(border)
    
    z_row = "|" + center("Z") + "|" + center(str(z)) + "|"
    for y in range(len(matrix[0])):
        z_row += center(str(z_vector[y])) + "|"
    print(z_row)
    print(border)
    
    co_row = "|" + center("CO") + "|" + center("-") + "|"
    for y in range(len(matrix[0])):
        co_row += center(str(co_vector[y])) + "|"
    print(co_row)
    print(border)

def noNegative(vector):
    for value in vector:
        if value < 0: return False
    return True


def find_res_row(b_vector):
    min = 1
    res = 0
    for i in range(len(b_vector)):
        if b_vector[i] < min: 
            min = b_vector[i]
            res = i
    return res


def compute_co(row, basis, z_vector):
    co = []
    for i in range(len(z_vector)):
        if i in basis: 
            co.append("-")
        else:
            co.append(abs(z_vector[i]/row[i]))
    return co

def find_res_col(co_vector):
    max = -1
    res = 0
    for i in range(len(co_vector)):
        if co_vector[i] != "-" and co_vector[i] > max: 
            max = co_vector[i]
            res = i
    return res

def AmbivalentSimplex(matrix, b_vector, z_vector, target):
    # ШАГ 1: 
    # Домножаем строки матрицы на -1 при необходимости.
    # Формируем базис
    step = 0
    basis = []
    z_answ = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] == -1 or matrix[x][y] == 1:
                if (isBasic(x, y, matrix)):
                    basis.append(y)
                    if matrix[x][y] < 0:
                        mulRowVal(matrix[x], -1)
                        b_vector[x] *= -1
                    break
    # ШАГ 2: 
    # Формируем Z-строку
    z_sign = -1 * target
    for z in z_vector: 
        z *= z_sign
    
    # ШАГ 3: 
    # Основной цикл поиска решения:
    while(not noNegative(b_vector)):
        step+=1
        print("ШАГ " + str(step) + ":")
        resolve_row = find_res_row(b_vector)
        co_vector = compute_co(matrix[resolve_row], basis, z_vector)
        resolve_col = find_res_col(co_vector)
        printTable(matrix, basis, b_vector, z_vector, z_answ, co_vector, rr, rc)
        print(f'Разрешающий элемент: {matrix[resolve_row][resolve_col]}')
        print(f'Выводим из базиса x{resolve_row}')
        print(f'Вводим в базис x{resolve_col}')


if __name__ == "__main__":
    path = ".\examples"
    print(80 * "-")
    print( (20 * " ") + "РГР" + (20 * " "))
    print( (10 * " ") + "Решение ЗЛП двойственным симплекс-методом" + (20 * " "))
    print(80 * "-")
    while(1):
        print("\nВведите имя файла с матрицей (или exit, чтобы выйти): ")
        name = input()
    
        if (name == "exit"):
            print("Завершение работы...")
            break
    
        if not name.__contains__(".txt"):
            name = name + ".txt"
        f_matrix = open(f'{path}\{name}', "r")
        s_matrix = f_matrix.read()
        f_matrix.close()

        matrix, b_vector, z_vector, target = parse_matrix(s_matrix)
        AmbivalentSimplex(matrix, b_vector, z_vector, target)

        

        
        
