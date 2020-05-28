import py2neo
from py2neo.internal.operations import create_subgraph
a = py2neo.Node("Person", name="Alice")
b = py2neo.Node("Person", name="Bob")
ab = py2neo.Relationship(a, "KNOWS", b)
ac = py2neo.Relationship(a, "KNO", b)
c = ab | ac
d = create_subgraph(c)
print(type(d))
print(type(c))