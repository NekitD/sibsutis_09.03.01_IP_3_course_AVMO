import math
from itertools import combinations
from Fract import Fract
from MatrixFunctions import parse_matrix


def isBasic(x, y, matrix):
    for i in range(matrix[x]):
        if ((i != y) and (matrix[x][i]) != 0):
            return False
    return True

def mulRowVal(row, b, val):
    for i in range(len(row)):
        row[i] *= -1

def printTable(matrix, basis, b_vector, z_vector, z, co_vector):
    strng = ""
    strng = (" " * 2) + "|" + "   " + "Б.п" + "   " + "|" + "   " + "1" + "   "
    
    for x in range(len(matrix)):
        strng += "|" + "    " + "x" + str(x) + "    " + "|"
    print("====" * len(matrix) + 2)
    print(strng)
    print("====" * len(matrix) + 2)
    strng = ""
    
    for y in len(basis):
        strng = (" " * 2) + "|" + "   " + "x" + str(basis[y]) + "   " + "|" + "   " 
        + str(b_vector[basis[y]]) + "   "
        for x in range(len(matrix)):
            strng += "|" + "    " + str(matrix[x][basis[y]]) + "    " + "|"
        print(strng)
        print("----" * len(matrix) + 2)
        strng = ""
    
    strng = (" " * 2) + "|" + "   " + "Z" + "   " + "|" + "   " 
    + str(z) + "   "
    for x in range(len(matrix)):
        strng += "|" + "    " + str(z_vector[x]) + "    " + "|"
    print(strng)

    strng = (" " * 2) + "|" + "   " + "CO" + "   " + "|" + "   " 
    + "-" + "   "
    for x in range(len(matrix)):
        strng += "|" + "    " + str(co_vector[x]) + "    " + "|"
    print(strng)


def noNegative(vector):
    for value in vector:
        if value < 0: return False
    return True


def find_res_row(b_vector):
    min = 1
    res = 0
    for i in len(b_vector):
        if b_vector[i] < min: 
            min = b_vector[i]
            res = i
    return res


def compute_co(row, z_vector):
    co = []
    for i in range(len(z_vector)):
        co.append(abs(z_vector[i]/row[i]))
    return co

def find_res_col(co_vector):
    max = -1
    res = 0
    for i in len(co_vector):
        if co_vector[i] > max: 
            max = co_vector[i]
            res = i
    return res

def AmbivalentSimplex(matrix, b_vector, z_vector, target):
    # ШАГ 1: 
    # Домножаем строки матрицы на -1 при необходимости.
    # Формируем базис
    basis = []
    z_answ = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] == -1 or matrix[x][y] == 1:
                if isBasic(x, y, matrix):
                    basis.append(x)
                    if matrix[x][y] < 0:
                        mulRowVal(matrix[x])
                        b_vector[x] *= -1
    # ШАГ 2: 
    # Формируем Z-строку
    z_sign = -1 * target
    for z in z_vector: 
        z *= z_sign
    
    # ШАГ 3: 
    # Основной цикл поиска решения:
    while(not noNegative(b_vector)):
        resolve_row = find_res_row(b_vector)
        co_vector = compute_co(resolve_row, z_vector)
        resolve_col = find_res_col(co_vector)
        printTable(matrix, basis, b_vector, z_vector, z_answ, co_vector)
        break # test


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

        

        
        
