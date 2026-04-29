import math
from itertools import combinations
from Fract import Fract
from MatrixFunctions import parse_matrix, print_matrix


class Method:
    def __init__(self):
        print("")



if __name__ == "__main__":
    path = ".\matrix"
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

        m_left, m_right = parse_matrix(s_matrix)
    
        print("\nИсходная матрица:")
        print_matrix(m_left, m_right)
        print()


        # left_copy = [[m_left[i][j] for j in range(len(m_left[0]))] for i in range(len(m_left))]
        # right_copy = m_right[:]
        

        
        
