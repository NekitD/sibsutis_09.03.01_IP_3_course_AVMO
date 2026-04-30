from Fract import Fract

def parse_matrix(matrix_str):
    rows = matrix_str.strip().split('\n')
    finish = False
    matrix = []  
    b_vector = [] 
    z_vector = []  
    target = 0
    
    for row in rows:
        row = row.strip()
        if not row: 
            continue
            
        if row == 'Z:':
            finish = True
            continue
            
        if not finish:
            if '|' not in row:
                continue
                
            s_matrix, right = row.split('|')
            left_parts = s_matrix.strip().split()
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
        
            matrix.append(left_part)
            b_vector.append(right_part)
        else:
            if '|' not in row:
                continue
                
            zs, starget = row.split('|')
            if "max" in starget:
                target = 1
            elif "min" in starget:
                target = -1
                
            zs_parts = zs.strip().split()
            for num in zs_parts:
                if '/' in num:
                    up, low = map(int, num.split('/'))
                    z_vector.append(Fract(up, low))
                else:
                    z_vector.append(Fract(int(num)))
    
    return matrix, b_vector, z_vector, target