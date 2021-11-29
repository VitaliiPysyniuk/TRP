import json
import numpy as np
import string
from prettytable import PrettyTable

class RootNode:
    def __init__(self):
        self.alternatives = []

    def choose_alternative(self):
        alternatives_balance = list()
        for alternative in self.alternatives:
            alternatives_balance.append(alternative.sub_balance)
        alternatives_balance = np.array(alternatives_balance)

        return np.argmax(alternatives_balance)


class Node:
    def __init__(self, alternative):
        self.probability: float = alternative['probability']
        self.balance: int = alternative['balance']
        # self.description = alternative['description']
        self.left_child: Node = None
        self.right_child: Node = None
        self.sub_balance: int = alternative['balance']

    def execute_balance_recalculation(self):
        if self.left_child:
            self.sub_balance += self.left_child.execute_balance_recalculation()
        if self.right_child:
            self.sub_balance += self.right_child.execute_balance_recalculation()
        self.sub_balance = self.sub_balance * self.probability

        return self.sub_balance


def add_children(node, curr_node_data):
    children = curr_node_data['children']
    for child in children:
        new_node = Node(child)
        if children.index(child) == 1:
            node.left_child = new_node
        else:
            node.right_child = new_node

        if 'children' in child:
            add_children(new_node, child)


if __name__ == '__main__':
    with open('lab_2_data.txt', encoding='utf8') as file:
        json_data = file.read()
        data = json.loads(json_data)

    root_node = RootNode()

    for alternative in data:
        new_alternative = Node(alternative)
        add_children(new_alternative, alternative)
        root_node.alternatives.append(new_alternative)
        root_node.alternatives[-1].execute_balance_recalculation()

    table = PrettyTable()
    table.field_names = ['Рішення', 'Прибуток']

    for i in range(len(root_node.alternatives)):
        row = [string.ascii_uppercase[i], root_node.alternatives[i].sub_balance]
        table.add_row(row)

    table.add_row(['', ''])
    table.add_row(['Найприбутковіша', string.ascii_uppercase[root_node.choose_alternative()]])
    print(table)

