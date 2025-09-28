def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    result = []
    
    for newCol in range(cols):
        newRow = []
        for iterator in range(rows):
            newRow.append(matrix[iterator][newCol])
        result.append(newRow)
    
    return result

def print_matrix(matrix, title):
    print(title)
    for row in matrix:
        print("   ", row)

print("Введите матрицу построчно. Числа в строке разделяйте пробелами. Для завершения ввода введите пустую строку.")

matrix = []
row_index = 1

while True:
    rowInput = input(f"\nСтрока {row_index}: ").strip()
    
    if not rowInput:
        break
    
    row = []
    for num_str in rowInput.split():
        row.append(int(num_str))
    
    matrix.append(row)
    row_index += 1

if matrix:
    transposed = transpose_matrix(matrix)
    print_matrix(transposed, "Транспонированная матрица")

