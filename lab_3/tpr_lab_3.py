from prettytable import PrettyTable
import numpy as np


def method_condorce(matrix):
    table = PrettyTable()
    # table.hrules = 1
    table.title = 'Метод Кондорсе'
    table.field_names = ['Пара', 1, 2, 3, 4, 5, 6, 'Σ']
    free_row = ['', '', '', '', '', '', '', '']

    candidates = matrix[0][0:-1]
    comparison_matrix = [[-1] * len(candidates) for i in range(len(candidates))]
    for i in range(len(matrix[0]) - 1):
        comparison_matrix[i][i] = 1

    candidates_pairs = list()
    for i in range(len(candidates)):
        for j in range(len(candidates) - i - 1):
            pair = list()
            pair.append(candidates[i])
            pair.append(candidates[j + 1 + i])
            candidates_pairs.append(pair)

    winner_is_found = False
    for pair in candidates_pairs:
        first_row = [f'{pair[0]}>{pair[1]}']
        second_row = [f'{pair[1]}>{pair[0]}']
        first_sum_of_votes = 0
        second_sum_of_votes = 0

        for i in range(len(comparison_matrix)):
            if min(comparison_matrix[i]) == 1:
                winner_is_found = True

        if winner_is_found:
            break

        for i in range(len(matrix)):
            if matrix[i].index(pair[0]) < matrix[i].index(pair[1]):
                first_row.append(matrix[i][-1])
                second_row.append('')
                first_sum_of_votes += matrix[i][-1]
            else:
                second_sum_of_votes += matrix[i][-1]
                second_row.append(matrix[i][-1])
                first_row.append('')

        first_row.append(first_sum_of_votes)
        second_row.append(second_sum_of_votes)
        table.add_row(first_row)
        table.add_row(second_row)
        table.add_row(free_row)

        first_candidate_index = candidates.index(pair[0])
        second_candidate_index = candidates.index(pair[1])
        if first_sum_of_votes > second_sum_of_votes:
            comparison_matrix[first_candidate_index][second_candidate_index] = 1
        else:
            comparison_matrix[second_candidate_index][first_candidate_index] = 1

    winner_index = -1
    for i in range(len(comparison_matrix)):
        if min(comparison_matrix[i]) == 1:
            winner_index = i

    print(table)

    return candidates[winner_index]


def method_borda(matrix):
    candidates = matrix[0][0:-1]
    candidates_votes = [0] * len(candidates)

    table = PrettyTable()
    # table.hrules = 1
    table.title = 'Метод Борда'
    table.field_names = ['Перевага'] + candidates

    for i in range(len(matrix)):
        row = ['>'.join(matrix[i][0:-1])]
        for j in range(len(candidates)):
            row.append(matrix[i][-1] * (3 - matrix[i].index(candidates[j])))
            candidates_votes[j] += matrix[i][-1] * (3 - matrix[i].index(candidates[j]))
        table.add_row(row)

    table.add_row((['Σ'] + candidates_votes))
    print(table)
    candidates_votes = np.array(candidates_votes)
    return candidates[np.argmax(candidates_votes)]


if __name__ == '__main__':
    with open('lab_3_data.txt', 'r') as file:
        lines = file.readlines()
        lines = [line[0:-1].split('>') for line in lines]
        for i in range(len(lines)):
            lines[i][-1] = int(lines[i][-1])

    input_matrix = lines
    # input_matrix = [
    #     ['A', 'B', 'C', 23],
    #     ['A', 'C', 'B', 33],
    #     ['B', 'A', 'C', 17],
    #     ['B', 'C', 'A', 16],
    #     ['C', 'A', 'B', 19],
    #     ['C', 'B', 'A', 18],
    # ]

    table = PrettyTable()
    # table.hrules = 1
    table.title = 'Результати голосування'
    table.field_names = ['Метод', 'Переможець']
    table.add_row(['Кондорсе', f'Кандидат {method_condorce(input_matrix)}'])
    table.add_row(['Борда', f'Кандидат {method_borda(input_matrix)}'])
    print(table)
