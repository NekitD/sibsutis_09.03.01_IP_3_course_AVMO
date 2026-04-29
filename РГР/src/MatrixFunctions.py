import Fract

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