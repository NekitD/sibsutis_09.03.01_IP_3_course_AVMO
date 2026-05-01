import math
from itertools import combinations
from Fract import Fract
from MatrixFunctions import parse_matrix
import numpy as np
import time
import copy


def print_problem(matrix, b_vector, z_vector, target, alt):
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Вывод целевой функции
    if alt:
        print("-Z = ", end="")
        target *= -1
    else:
        print("Z = ", end="")
    first = True
    for j in range(cols):
        if z_vector[j] != 0:
            k = z_vector[j]
            if not first and k > 0:
                print(" + ", end="")
            elif not first and k < 0:
                print(" - ", end="")
            elif first and k < 0:
                print("-", end="")
            
            abs_k = abs(k)
            if abs_k == 1:
                print(f"x{j+1}", end="")
            else:
                print(f"{abs_k}*x{j+1}", end="")
            first = False
    
    if target > 0:
        print(" -> max")
    else:
        print(" -> min")
    
    # Вывод ограничений
    for i in range(rows):
        print("| ", end="")
        first = True
        for j in range(cols):
            if matrix[i][j] != 0:
                k = matrix[i][j]
                if not first and k > 0:
                    print(" + ", end="")
                elif not first and k < 0:
                    print(" - ", end="")
                elif first and k < 0:
                    print("-", end="")
                
                abs_k = abs(k)
                if abs_k == 1:
                    print(f"x{j+1}", end="")
                else:
                    print(f"{abs_k}*x{j+1}", end="")
                first = False
        
        print(f" = {b_vector[i]}")



def isBasic(x, y, matrix, z_vector):
    for i in range(len(matrix)):
        if ((i != x) and (matrix[i][y]) != 0):
            return False
    if z_vector[y] != 0:
        return False
    return True

def mulRowVal(row, val):
    for i in range(len(row)):
        row[i] *= val

def printTable(matrix, basis, b_vector, z_vector, z, co_vector, rr, rc, target):
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
    
    z_row = "|"
    if target > 0: 
        z_row += center("Z")
    else:
        z_row += center("-Z")
    z_row += "|" + center(str(z)) + "|"

    for y in range(len(matrix[0])):
        z_row += center(str(z_vector[y])) + "|"
    print(z_row)
    print(border)
    
    co_row = "|" + center("CO") + "|" + center("-") + "|"
    if(co_vector):
        for y in range(len(matrix[0])):
            co_row += center(str(co_vector[y])) + "|"
    else:
        for y in range(len(matrix[0])):
            co_row += center("-") + "|"
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
        if i in basis or row[i] >= 0: 
            co.append("-")
        else:
            co.append(abs(z_vector[i]/row[i]))
    return co

def find_res_col(co_vector):
    min = None
    res = -1
    for i in range(len(co_vector)):
        if not isinstance(co_vector[i], str):
            min = co_vector[i]
            res = i
            break
    if res < 0:
        return res
    for i in range(len(co_vector)):
        if co_vector[i] != "-" and co_vector[i] < min: 
            min = co_vector[i]
            res = i
    return res


def new_table(old_matrix, old_b_vector, old_z_vector, old_z_answ, rr, rc, old_basis):
    rows = len(old_matrix)
    cols = len(old_matrix[0])
    
    matrix = [[Fract(0) for _ in range(cols)] for _ in range(rows)]
    b_vector = [Fract(0) for _ in range(rows)]
    z_vector = [Fract(0) for _ in range(cols)]
    basis = old_basis[:]
    basis[rr] = rc
    
    # Делим разрешающую строку на разрешающий элемент
    for col in range(cols):
        matrix[rr][col] = old_matrix[rr][col] / old_matrix[rr][rc]

    # Метод прямоугольников (матрица)
    for x in range(rows):
        for y in range(cols):
            if x == rr or y == rc: continue
            matrix[x][y] = old_matrix[x][y] - ((old_matrix[rr][y] * old_matrix[x][rc]) / old_matrix[rr][rc])
    
    # Метод прямоугольников (z-строка)
    for y in range(cols):
        if y != rc:
            z_vector[y] = old_z_vector[y] - ((old_matrix[rr][y] * old_z_vector[rc]) / old_matrix[rr][rc])
    
    # Метод прямоугольников (b-строка)
    for x in range(rows):
        if x == rr: 
            b_vector[x] = old_b_vector[x]/old_matrix[rr][rc]
        else:
            b_vector[x] = old_b_vector[x] - ((old_b_vector[rr] * old_matrix[x][rc]) / old_matrix[rr][rc])

    # Метод прямоугольников (Ответ)
    z_answ = old_z_answ - ((old_z_vector[rc] * old_b_vector[rr]) / old_matrix[rr][rc])
    return matrix, b_vector, z_vector, basis, z_answ, 


def solution(b_vector, z_vector, basis, z_answ, target):
    sol = "Z("
    for i in range(len(z_vector) - len(b_vector)):
        if i in basis:
            sol += str(b_vector[basis.index(i)])
        else:
            sol += "0"
        if i < len(z_vector) - len(b_vector) - 1:
            sol += ", "
    sol += ")"
    sol += " = "
    sol += str(z_answ*target)
    return sol

def com_solution(b_vector, z_vector, basis, z_answ, target):
    sol = "Z("


def isInf(z_vector, basis):
    for i in range(len(z_vector)):
        if (z_vector[i] == 0) and (i not in basis):
            return True
    return False

#================================================================================================
def AmbivalentSimplex(matrix, b_vector, z_vector, target):
    
    NO_SOLUTION = -1
    ONE_SOLUTION = 0
    INF_SOLUTION = 1
    status = ONE_SOLUTION

    print()
    print("Исходная задача:")
    print_problem(matrix, b_vector, z_vector, target, False)
    print()
    # ШАГ 1: 
    # Домножаем строки матрицы на -1 при необходимости.
    # Формируем базис
    step = 0
    basis = []
    z_answ = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] == -1 or matrix[x][y] == 1:
                if (isBasic(x, y, matrix, z_vector)):
                    basis.append(y)
                    if matrix[x][y] < 0:
                        mulRowVal(matrix[x], -1)
                        b_vector[x] *= -1
                    break

    print("Преобразованная задача:")
    for i in range(len(z_vector)):
        z_vector[i] *= target
    if target > 0:
        print_problem(matrix, b_vector, z_vector, target, False)
    else:
        print_problem(matrix, b_vector, z_vector, target, True)
    print()

    # ШАГ 2: 
    # Формируем Z-строку в таблице
    for i in range(len(z_vector)):
        z_vector[i] *= -1
    
    # ШАГ 3: 
    # Основной цикл поиска решения:
    while(True):
        step+=1
        end = noNegative(b_vector)
        print()
        print("Таблица № " + str(step) + ":")
        if end:
            resolve_row = None
            resolve_col = None
            co_vector = None
        else:
            resolve_row = find_res_row(b_vector)
            co_vector = compute_co(matrix[resolve_row], basis, z_vector)
            resolve_col = find_res_col(co_vector)
            if resolve_col < 0: status = NO_SOLUTION
            if isInf(z_vector, basis): status = INF_SOLUTION
        printTable(matrix, basis, b_vector, z_vector, z_answ, co_vector, resolve_row, resolve_col, target)
        print("Соответствующее решение:")
        print(solution(b_vector, z_vector, basis, z_answ, target))
        if(end or status == NO_SOLUTION): break
        print()
        print(f'Разрешающий элемент: {matrix[resolve_row][resolve_col]}')
        print(f'Выводим из базиса x{basis[resolve_row] + 1}')
        print(f'Вводим в базис x{resolve_col + 1}')
        matrix, b_vector, z_vector, basis, z_answ = new_table(matrix, b_vector, z_vector, z_answ, resolve_row, resolve_col, basis)
    
    # ШАГ 4: Вывод итогового решения
    print()
    print("Итоговое решение:")
    
    if status == NO_SOLUTION:
        print("Нет решения!")
        return
    
    if status == INF_SOLUTION:
        print("Решений бесконечно много:")

    answer = "Z_"
    if target > 0:
        answer += "max"
    else:
        answer += "min"
    answer += " = "

    if status == INF_SOLUTION:
        answer += com_solution(b_vector, z_vector, basis, z_answ, target)
    else:
        answer += solution(b_vector, z_vector, basis, z_answ, target)
    print(answer)
#================================================================================================

if __name__ == "__main__":
    path = ".\examples"
    print(80 * "-")
    print( (30 * " ") + "РГР" + (30 * " "))
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

        

        
        
