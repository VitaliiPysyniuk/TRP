from prettytable import PrettyTable
import numpy as np
import random


def wald_criteria(matrix):
    return np.min(matrix, axis=1)


def laplace_criteria(matrix):
    return [round(sum(row) / len(row), 3) for row in matrix]


def savage_criteria(matrix):
    return np.max(matrix, axis=1)


def hurwitz_criteria(matrix, lambda_value=None):
    lambda_value = lambda_value if lambda_value else random.randint(1, 9) / 10
    return [lambda_value * max(row) + (1 - lambda_value) * min(row) for row in matrix]


def bayes_laplace_criteria(matrix, p):
    return [sum(np.array(matrix[i]) * np.array(p)) for i in range(len(matrix))]


if __name__ == '__main__':
    with open('lab_1_data.txt', 'r') as file:
        lines = file.readlines()
        lines = [line[0:-1].split(',') for line in lines]
        lines = [[float(value) for value in row] for row in lines]

    value_matrix = np.array(lines[0:-1])
    possibilities = lines[-1]

    wald_res = wald_criteria(value_matrix)
    savage_res = savage_criteria(value_matrix)
    laplace_res = laplace_criteria(value_matrix)
    hurwitz_res = hurwitz_criteria(value_matrix, lambda_value=0.4)
    bayes_laplace_res = bayes_laplace_criteria(value_matrix, possibilities)

    table = PrettyTable()
    table.add_column('Можливі альтернативні рішення',
                     ['', 'Прод роботу в звичному режимі', 'Активув рекламну діяльність', 'Активув рекламу і '
                                                                                          'знизити ціну'])

    table.add_column('Можливі стани ', (['Конк на тому ж рівні'] + list(value_matrix.transpose()[0])))
    table.add_column('зовнішнього', (['Конк трішки посилилась'] + list(value_matrix.transpose()[1])))
    table.add_column('середовища', (['Конк різко посилилась'] + list(value_matrix.transpose()[2])))

    table.add_column('Критерії', (['Вальда'] + list(wald_res)))
    table.add_column('', (['Севіджа'] + list(savage_res)))
    table.add_column('', (['Лапласа'] + list(laplace_res)))
    table.add_column('', (['Гурвіца'] + list(hurwitz_res)))
    table.add_column('', (['Байеса-Лапласа'] + list(bayes_laplace_res)))

    # table.hrules = 1
    print(table)

    print('\nНайкращі рішення:')
    print(f'За критерієм Вальда альтернатива: {np.argmax(wald_res) + 1}')
    print(f'За критерієм Севіджа альтернатива: {np.argmin(savage_res) + 1}')
    print(f'За критерієм Лапласа альтернатива: {np.argmax(laplace_res) + 1}')
    print(f'За оцінкою Гурвіца альтернатива: {np.argmax(hurwitz_res) + 1}')
    print(f'За оцінкою Байеса-Лапласа альтернатива: {np.argmax(bayes_laplace_res) + 1}')
