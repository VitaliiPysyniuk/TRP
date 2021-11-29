from prettytable import PrettyTable
import numpy as np
import string


def evaluation(data):
    table = PrettyTable()
    field_names = ['Номер', 'Параметр', 'Вага']
    for i in range(1, len(data)):
        field_names.append(string.ascii_uppercase[i - 1])
        field_names.append('Оцінка ' + string.ascii_uppercase[i - 1])
    table.field_names = field_names

    weight_mark_value = [0] * (len(data) - 1)

    last_row = ['Середня оцінка', '', '']
    for i in range(len(data[0]['parameters'])):
        row = [i + 1]
        for j in range(len(data)):
            row.append(data[j]['parameters'][i])
            row.append(data[j]['marks'][i])
            weight_mark_value[j - 1] += data[j]['marks'][i] * data[0]['marks'][i]

            if j != 0 and i == (len(data[0]['parameters']) - 1):
                last_row.append('')
                last_row.append(round(sum(data[j]['marks']) / len(data[j]['marks']), 3))
        table.add_row(row)

    table.add_row(([''] * (len(data) * 2 + 1)))
    new_weight_mark_value = ['Оцінка з вагою', '', '']
    for value in weight_mark_value:
        new_weight_mark_value.append('')
        new_weight_mark_value.append(round(value, 3))

    table.add_row(last_row)
    table.add_row(new_weight_mark_value)
    print(table)

    winner = data[np.argmax(weight_mark_value) + 1]
    winner['total_mark'] = np.max(weight_mark_value)
    return winner


if __name__ == '__main__':
    with open('lab_4_data.txt', 'r', encoding='utf8') as file:
        lines = file.readlines()
        lines = [line[0:-1].split(',') for line in lines]

    input_data = []
    for i in range(0, int(len(lines) - 1), 2):
        data_object = {}
        data_object['parameters'] = lines[i]
        marks = list()
        for mark in lines[i + 1]:
            marks.append(float(mark))
        data_object['marks'] = marks
        input_data.append(data_object.copy())

    result = evaluation(input_data)

    table = PrettyTable()
    table.title = 'Результат оцінювання'
    table.field_names = ['Параметр', 'Експертна оцінка']
    for i in range(len(result['parameters'])):
        row = list()
        row.append(result['parameters'][i])
        row.append(result['marks'][i])
        table.add_row(row)
    table.add_row(['', ''])
    table.add_row(['Оцінка з врахуванням ваги', result['total_mark']])
    print(table)

