import math
from itertools import combinations
from Fract import Fract
from MatrixFunctions import parse_matrix


class Method:
    def __init__(self, matrix, b_vector, z_vector, target):
        self.matrix = matrix
        self.b_vector = b_vector 
        self.z_vector = z_vector
        self.target = target
        self.co = []

    def print_table(self):
        print("")

    def __str__(self):
        return ""

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
        solution = Method(matrix, b_vector, z_vector, target)
        print(solution)

        

        
        
