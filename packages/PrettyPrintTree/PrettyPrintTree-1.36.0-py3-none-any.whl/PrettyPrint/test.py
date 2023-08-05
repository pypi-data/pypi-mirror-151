from PrintTree import PrettyPrintTree


class Graph:
    def __init__(self, value):
        self.val = value
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        return neighbor


class Tree:
    def __init__(self, value, label=None):
        self.val = value
        self.children = []
        self.label = label

    def add_child(self, child):
        self.children.append(child)
        return child


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"""Person {{ 
    age: {self.age}, 
    name: {self.name} 
}}"""

# border: bool = False,
# max_depth: int = -1,

from colorama import Back
print()
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label)

tree = Tree("STATISTIC TREE")
child0 = tree.add_child(Tree("work"))
child1 = tree.add_child(Tree("go fishing"))
child0.add_child(Tree("keep job", label="75%"))
child0.add_child(Tree("lose job", label="25%"))
child1.add_child(Tree("catch fish", label="64%"))
child1.add_child(Tree("fail to catch fish", label="36%"))
pt(tree)

print()
print()
# some_json = [{'foo': {'a': 1, 'b': 2}, 'bar': (['a', 'a2'], 'b'), 'qux': {'foo': 1, 'bar': [{'a': 1, 'b': 2}, 'b']}}, 1]
some_json = {'foo': 1, 'bar': ('a', 'b'), 'qux': {'foo': 1, 'bar': ['a', 'b']}}

pt = PrettyPrintTree()
pt(some_json)

# from PrettyPrint import print_graph
#
# gr1 = Graph("111111\n1111111")
# gr2 = gr1.add_neighbor(Graph("22222\n22222"))
# gr3 = gr1.add_neighbor(Graph("33333333\n33333333"))
# gr3.add_neighbor(gr2)
# gr4 = gr2.add_neighbor(Graph("4444444\n4444444"))
# gr4.add_neighbor(gr1)
# # gr4.add_neighbor(gr2)
# print_graph(gr1, get_neighbors=lambda x: x.neighbors, get_val=lambda x: x.val)

