def parse_matrix(matrix_str):
    rows = matrix_str.strip().split('\n')
    left_matrix = []  
    right_vector = []  
    for row in rows:
        left, right = row.strip().split('|')

        left_part = list(map(float, left.strip().split()))
        right_part = float(right.strip())

        left_matrix.append(left_part)
        right_vector.append(right_part)
    return left_matrix, right_vector

def print_matrix(left, right):
    for i in range(len(left)):
        print(*[f"{x:8.2f}" for x in left[i]], f" | {right[i]:8.2f}")

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