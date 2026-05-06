from Fract import Fract
from MatrixFunctions import parse_matrix

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


def com_solution(solutions, final_basis, z_vector, z_answ, target):
    num_vars = len(z_vector)
    num_basis = len(final_basis)
    num_real_vars = num_vars - num_basis
    
    # Все решения
    all_solutions = []

    for b_vec, basis, answer in solutions:
        if not noNegative(b_vec):
            continue
        sol_vec = [Fract(0) for _ in range(num_real_vars)]
        for i, var in enumerate(basis):
            if var < num_real_vars:
                sol_vec[var] = b_vec[i]

        if noNegative(sol_vec) and sol_vec not in all_solutions and answer == z_answ:
            all_solutions.append(sol_vec)

    # Фильтр нулевого решения
    non_zero_solutions = []
    for sol in all_solutions:
        good = False
        for v in sol:
            if v != 0:
                good = True
                break
        if good:
            non_zero_solutions.append(sol)
    
    if len(non_zero_solutions) >= 2:
        all_solutions = non_zero_solutions
    
    # Сортировка решений по x1
    all_solutions.sort(key=lambda x: float(x[0]))
    
    sol_min = all_solutions[0]  # решение с минимальным x1
    sol_max = all_solutions[-1]  # решение с максимальным x1

    # print("DEBUG MIN SOL:", end=" ")
    # for i in sol_min:
    #     print(i, end=" ")
    # print()
    # print("DEBUG MAX SOL", end=" ")
    # for i in sol_max:
    #     print(i, end=" ")
    # print()
    # Разица между макс. и мин. для каждого x
    diff = []
    for i in range(num_real_vars):
        d = sol_max[i] - sol_min[i]
        diff.append(d)
    
    # Формирование ответа
    result = "Z("
    for j in range(num_real_vars):
        if diff[j] == 0:
            # Переменная не меняется
            result += str(sol_min[j])
        else:
            # Переменная меняется
            if diff[j] > 0:
                if diff[j] == 1:
                    result += f"{sol_min[j]} + λ"
                else:
                    result += f"{sol_min[j]} + {diff[j]}*λ"
            else:
                abs_diff = abs(diff[j])
                if abs_diff == 1:
                    result += f"{sol_min[j]} - λ"
                else:
                    result += f"{sol_min[j]} - {abs_diff}*λ"
        
        if j < num_real_vars - 1:
            result += ", "
    
    result += f") = {z_answ * target}"
    result += f"\nгде λ ∈ [0, 1] - параметр"
    
    return result

def isInf(z_vector, basis):
    for i in range(len(z_vector)):
        if (z_vector[i] == 0) and (i not in basis):
            return True
    return False

def printTableSim(matrix, basis, b_vector, z_vector, z, co_vector, rr, rc, target):
    col_width = 12
    def center(text, width=col_width):
        text = str(text)
        if len(text) > width:
            return text[:width-3] + "..."
        return text.center(width)
    
    num_cols = len(matrix[0])
    
    border = "+" + "-" * col_width + "+" + "-" * col_width + "+"
    for _ in range(num_cols):
        border += "-" * col_width + "+"
    border += "-" * col_width + "+" 
    print(border.replace("-", "="))
    
    header = "|" + center("Б.п") + "|" + center("1") + "|"
    for i in range(num_cols):
        header += center(f"x{i+1}") + "|"
    header += center("CO") + "|"
    print(header)
    print(border.replace("-", "="))
    
    for x in range(len(basis)):
        row = "|" + center(f"x{basis[x]+1}") + "|" + center(str(b_vector[x])) + "|"
        for y in range(len(matrix[x])):
            if x == rr and y == rc:
                row += center(f'[{matrix[x][y]}]') + "|"
            else:
                row += center(str(matrix[x][y])) + "|"
        if co_vector and x < len(co_vector):
            row += center(str(co_vector[x])) + "|"
        else:
            row += center("-") + "|"
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
    z_row += center("-") + "|" 
    print(z_row)
    print(border)


#----------------------------------------------------------
def find_res_col_sim(z_vector, basis):
    max_val = None
    res = -1
    for i in range(len(z_vector)):
        if i not in basis and z_vector[i] <= 0: 
            if max_val is None or z_vector[i] > max_val:
                max_val = z_vector[i]
                res = i
    return res

def compute_co_sim(col, b_vector):
    co = []
    for i in range(len(b_vector)):
        if col[i] <= 0: 
            co.append("-")
        else:
            co.append(b_vector[i]/col[i])
    return co

def find_res_row_sim(co_vector):
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
    
    x_sols = []
    # ШАГ 3: 
    # Основной цикл поиска решения:
    accomp = False
    while(True):
        step+=1
        end = noNegative(b_vector)
        x_sols.append([b_vector, basis, z_answ])
        print()
        # print("Таблица № " + str(step) + ":")
        if end:
            if (status == INF_SOLUTION) and (accomp):
                resolve_col = None 
                resolve_row = None
                print("Таблица № " + str(step - 1) + ":")
                printTable(matrix, basis, b_vector, z_vector, z_answ, co_vector, resolve_row, resolve_col, target)
                resolve_col = find_res_col_sim(z_vector, basis)
                resolve_col_content = []
                for x in range(len(matrix)):
                    resolve_col_content.append(matrix[x][resolve_col])
                co_vector = compute_co_sim(resolve_col_content, b_vector)
                resolve_row = find_res_row_sim(co_vector)
                print()
                print("Таблица № " + str(step - 1) + " (Обычным симплекс-методом):")
                printTableSim(matrix, basis, b_vector, z_vector, z_answ, co_vector, resolve_row, resolve_col, target)
                print("Соответствующее решение:")
                print(solution(b_vector, z_vector, basis, z_answ, target))
                print()
                print(f'Разрешающий элемент: {matrix[resolve_row][resolve_col]}')
                print(f'Выводим из базиса x{basis[resolve_row] + 1}')
                print(f'Вводим в базис x{resolve_col + 1}')
                print()
                x_sols.append([b_vector, basis, z_answ])
                matrix, b_vector, z_vector, basis, z_answ = new_table(matrix, b_vector, z_vector, z_answ, resolve_row, resolve_col, basis)
                co_vector = None
                resolve_row = None
                resolve_col = None
                print("Таблица № " + str(step) + ":")
                printTableSim(matrix, basis, b_vector, z_vector, z_answ, co_vector, resolve_row, resolve_col, target)
                print("Соответствующее решение:")
                print(solution(b_vector, z_vector, basis, z_answ, target))
                print()
                x_sols.append([b_vector, basis, z_answ])
                accomp = False
            else:
                if status != INF_SOLUTION:
                    print("Таблица № " + str(step) + ":")
                    printTable(matrix, basis, b_vector, z_vector, z_answ, co_vector, resolve_row, resolve_col, target)
                    print("Соответствующее решение:")
                    print(solution(b_vector, z_vector, basis, z_answ, target))
                    break
                resolve_row = None
                resolve_col = None
                co_vector = None
                accomp = True
        else:
            resolve_row = find_res_row(b_vector)
            co_vector = compute_co(matrix[resolve_row], basis, z_vector)
            resolve_col = find_res_col(co_vector)
            if resolve_col < 0: status = NO_SOLUTION
            if isInf(z_vector, basis): status = INF_SOLUTION
            printTable(matrix, basis, b_vector, z_vector, z_answ, co_vector, resolve_row, resolve_col, target)
        
        if((end and accomp == False) or status == NO_SOLUTION): break
        print()
        if not accomp: 
            print(f'Разрешающий элемент: {matrix[resolve_row][resolve_col]}')
            print(f'Выводим из базиса x{basis[resolve_row] + 1}')
            print(f'Вводим в базис x{resolve_col + 1}')
            matrix, b_vector, z_vector, basis, z_answ = new_table(matrix, b_vector, z_vector, z_answ, resolve_row, resolve_col, basis)
    
    # ШАГ 4: Вывод итогового решения
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
        answer += com_solution(x_sols, basis, z_vector, z_answ, target)
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

        

        
        
