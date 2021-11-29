import math
import numpy


def change_variables(simplex_table, constraints):
    # next_basis_var_value = numpy.min(simplex_table[0].reverse())
    simplex_table_row = simplex_table[0].copy()
    simplex_table_row.reverse()
    next_basis_var_value = numpy.min(simplex_table_row)

    if next_basis_var_value >= 0:
        return

    next_basis_var_index = numpy.argmin(simplex_table_row)
    next_basis_var_index = len(simplex_table_row) - next_basis_var_index - 1

    # next_basis_var_index = simplex_table[0].index(next_basis_var_value)

    minimum = {"value": numpy.inf, "index": -1}
    for i in range(1, len(simplex_table)):
        if simplex_table[i][next_basis_var_index] <= 0:
            continue

        if (constraints[i] / simplex_table[i][next_basis_var_index]) < minimum["value"]:
            minimum["value"] = constraints[i] / simplex_table[i][next_basis_var_index]
            minimum["index"] = i

    return {"index_1": next_basis_var_index, "index_2": minimum["index"]}


def execute_switch(index_1, index_2, simplex_table, constraints):
    constraints[index_2] = constraints[index_2] / simplex_table[index_2][index_1]
    divide_on = simplex_table[index_2][index_1]
    for i in range(len(simplex_table[index_2])):
        simplex_table[index_2][i] = simplex_table[index_2][i] / divide_on

    for i in range(len(simplex_table)):
        if i == index_2 or simplex_table[i][index_1] == 0:
            continue

        new_row = [value * simplex_table[i][index_1] * (-1) for value in simplex_table[index_2]]
        constraints[i] = constraints[i] + (constraints[index_2] * simplex_table[i][index_1] * (-1))
        simplex_table[i] = [simplex_table[i][j] + new_row[j] for j in range(len(simplex_table[i]))]


def print_table(table, solutions, target_func, coefficients, variables):
    number_of_constraints = len(coefficients)
    title = ['   |   '] + [f'x{i + 1}   |   ' for i in range(len(target_func) + number_of_constraints)]
    title[-1] = title[-1][:-1]
    title = title + ['Рішення']
    title = ''.join(title)
    print(title)

    symbols = [' z'] + [f'x{i + 1 + len(target_func)}' for i in range(number_of_constraints)]
    for j in range(len(variables)):
        if variables[j] != -1:
            symbols[variables[j]] = f'x{j + 1}'

    for i in range(len(table)):
        print(f'{symbols[i]} |', end='')
        for value in table[i]:
            print(format(value, ' 3.4f'), end=' |')
        print(f" {format(solutions[i], ' 4.4f')}")


def create_simplex_table(target_function, coefficient_matrix):
    simplex = []
    number_of_constraints = len(coefficient_matrix)

    simplex.append([val * -1 for val in target_function] + ([0] * number_of_constraints))
    for i in range(number_of_constraints):
        additional_columns = [1 if i == j else 0 for j in range(number_of_constraints)]
        simplex.append(coefficient_matrix[i] + additional_columns)

    variables_row_index = [-1] * len(target_function)

    return simplex, variables_row_index


def simplex_method(target_func, coefficients, constraints, show=False):
    constraints = [0] + constraints

    simplex_table, variables = create_simplex_table(target_func, coefficients)
    show and print_table(simplex_table, constraints, target_func, coefficients, variables)

    while True:
        indexes = change_variables(simplex_table, constraints)
        if not indexes:
            break
        variables[indexes['index_1']] = indexes['index_2']
        execute_switch(**indexes, simplex_table=simplex_table, constraints=constraints)
        show and print('-------------------------------------------------------------------')
        show and print_table(simplex_table, constraints, target_func, coefficients, variables)

    show and print('-------------------------------------------------------------------')

    f = 0
    main_var = list()
    for i in range(len(variables)):
        if variables[i] == -1:
            show and print(f"x{i + 1} = {format(0, ' 3.4f')}")
            main_var.append(0)
            continue

        f += (constraints[variables[i]] * target_func[i])
        show and print(f"x{i + 1} = {format(constraints[variables[i]], ' 3.4f')}")
        main_var.append(constraints[variables[i]])

    show and print(f" f = {format(f, ' 3.4f')}")
    show and print('-------------------------------------------------------------------')

    result = {}
    result['func'] = f
    result['main'] = main_var
    result['add'] = simplex_table[0][len(variables):]

    return result


if __name__ == '__main__':
#     t = [1, 0, 0, 1, 1]
#     coef = [
#         [11, 0, 0, 14, 17],
#         [10, 0, 0, 16, 13],
#         [12, 0, 0, 11, 9]
#     ]
#     const = [1, 1, 1]

    t = [2, 1, 0, 0, 0]
    coef = [
        [1, 3, -1, 0, 0],
        [2, -2, 0, 1, 0],
        [-3, 4, 0, 0, 1]
    ]
    const = [6, 4, 3]

    res = simplex_method(t, coef, const, show=True)
    # print(res)
    # v = 1 / res['func']
    # print(res)
    # print(v)
    # sum = 0
    # for value in res['main']:
    #     sum += value * v
    #     print(value * v)

    print(sum)
