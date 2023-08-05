from PrintTree import PrettyPrintTree


class Graph:
    def __init__(self, value):
        self.val = value
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        return neighbor


class Tree:
    def __init__(self, value):
        self.val = value
        self.children = []

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
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, orientation=PrettyPrintTree.HORIZONTAL, border=True)
tree = Tree(1)
child2 = tree.add_child(Tree("2\n2\n2\n23562362362\n2\n3\n5\n2\n3\n5\n4"))
child0 = tree.add_child(Tree("1\n2"))
child0.add_child(Tree("!"))
child0.add_child(Tree("the\nsame"))
child0.add_child(Tree(1))
child1 = tree.add_child(Tree({1: 2, '2h': 44}))
child2.add_child(Tree(5))
child2.add_child(Tree(6))
child2.add_child(Tree(7))

child2.add_child(Tree(Person("child Node", age=10)))
pt(tree)

print()
# some_json = [{'foo': {'a': 1, 'b': 2}, 'bar': (['a', 'a2'], 'b'), 'qux': {'foo': 1, 'bar': [{'a': 1, 'b': 2}, 'b']}}, 1]
some_json = {'foo': 1, 'bar': ('a', 'b'), 'qux': {'foo': 1, 'bar': ['a', 'b']}}

pt = PrettyPrintTree()
pt.print_json(some_json, name="my dictionary")

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

