import numpy as np
from lab_5.simplex_method import simplex_method
from prettytable import PrettyTable

def check_clean_strategies(matrix):
    alpha = np.max(np.min(matrix, axis=1))
    beta = np.min(np.max(matrix, axis=0))

    if alpha != beta:
        return [False, alpha, beta]

    row_index = np.argmax(np.min(matrix, axis=1))
    column_index = np.argmin(np.max(matrix, axis=0))

    return [True, row_index, column_index]


def simplify_matrix(matrix, item_type, l_c):
    if item_type == 'columns':
        matrix = matrix.transpose()
    to_delete = list()

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                continue
            matrix_subs = matrix[i] - matrix[j]
            if max(matrix_subs) < 0 and item_type == 'rows':
                to_delete.append(i)
                l_c[0][i] = 0
            elif min(matrix_subs) > 0 and item_type == 'columns':
                to_delete.append(i)
                l_c[1][i] = 0

    to_delete = list(set(to_delete))

    new_matrix = list()
    for i in range(len(matrix)):
        if i in to_delete:
            continue
        new_matrix.append(matrix[i])
    new_matrix = np.array(new_matrix)
    if item_type == 'columns':
        new_matrix = new_matrix.transpose()

    return [new_matrix, l_c]


def matrix_equal(matrix_1, matrix_2):
    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[0])):
            if matrix_1[i][j] != matrix_2[i][j]:
                print(matrix_1[i][j])
                print(matrix_2[i][j])
                return False

    return True


def find_optimal_solution(matrix, matrix_size, l_c):
    new_matrix = list()
    skipped_rows = 0
    for i in range(matrix_size[0]):
        if l_c[0][i] == 0:
            skipped_rows += 1
            new_matrix.append([0] * matrix_size[1])
            continue

        row = list()
        skipped_columns = 0
        for j in range(matrix_size[1]):
            if l_c[1][j] == 0:
                skipped_columns += 1
                row.append(0)
                continue

            row.append(matrix[i - skipped_rows][j - skipped_columns])
        new_matrix.append(row)

    new_matrix = np.array(new_matrix)

    target_function = l_c[1]
    coef = list()
    for i in range(len(new_matrix)):
        if l_c[0][i] == 0:
            continue
        coef.append(list(new_matrix[i]))
    const = [1] * len(coef)

    optimal_result = simplex_method(target_function, coef, const)
    y_variables = optimal_result['main']
    x_variables = list()
    v = round(1 / optimal_result['func'], 3)
    p = list()
    q = list()

    add_var = iter(optimal_result['add'])

    for i in range(len(l_c[0])):
        if l_c[0][i] == 0:
            x_variables.append(0)
        else:
            x_variables.append(next(add_var))

        p.append(round(x_variables[i] * v, 3))
        q.append(round(y_variables[i] * v, 3))

    return {'v': v, 'p': p, 'q': q}


def print_table(matrix, l_c):
    table = PrettyTable()
    row = ['']
    for i in range(len(l_c[1])):
        if l_c[1][i] != 0:
            row.append(f'B{i + 1}')
    table.field_names = row

    skipped_rows = 0
    for i in range(len(l_c[0])):
        row = list()
        if l_c[0][i] != 0:
            row.append(f'A{i + 1}')
            row = row + list(matrix[i - skipped_rows])
            table.add_row(row)
        else:
            skipped_rows += 1

    print(table)


if __name__ == '__main__':
    with open('lab_5_data.txt', 'r') as file:
        lines = file.readlines()
        lines = [[int(value) for value in line[0:-1].split(',')] for line in lines]

    input_matrix = np.array(lines)
    result = check_clean_strategies(input_matrix)
    print('Результати:')
    if not result[0]:
        print('Гра не має вирішення в чистих стратегіях, тому переходимо')
        print('до пошуку оптимального рішення в мішаних стратегіях')
        print(f'Ціна гри повинна становити: {result[1]} < V < {result[2]}\n')
        print('Спрощена матриця платежів має вигляд:')
        curr_type = 'rows'
        curr_matrix = input_matrix
        lines_and_columns = [
            [1] * len(curr_matrix),
            [1] * len(curr_matrix[0])
        ]

        while True:
            res = simplify_matrix(curr_matrix, curr_type, lines_and_columns)
            if np.array_equal(res[0], curr_matrix):
                break
            curr_type = 'columns' if curr_type == 'rows' else 'rows'
            lines_and_columns = res[1]
            curr_matrix = res[0]

        result = find_optimal_solution(curr_matrix, input_matrix.shape, lines_and_columns)
        print_table(curr_matrix, lines_and_columns)
        print('\nОптимальне рішення було знайдено за допомогою симплекс-методу:')
        print(f"Оптимальне значення ціни гри становить: {result['v']}")
        print(f"Оптимальні значення компонентів векторів мішаних стратегій:")
        print(f"для гравця A: p = {result['p']}  Σ = {sum(result['p'])}")
        print(f"для гравця В: q = {result['q']}  Σ = {sum(result['q'])}")


    else:
        print('Гра має вирішення в чистих стратегіях')
        print(f'Ціна гри становить: {input_matrix[result[1]][result[2]]}')
        print(f'Сідлова точка: ({result[1]}; {result[2]})')
