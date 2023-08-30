# https://gist.github.com/hirokai/9202782

from math import sqrt


class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

p1 = Point(10, 3)
p2 = Point(1, 0)

thisDict = {1: p1, 2:p2}
print(thisDict[2],'\n')

def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)

print(p1.x, p1.y, p2.x, p2.y)
print(distance(p1,p2))

p2.shift(2,3)

print(p2)


class Var(object):
    """
    Node of an equation system solver that represents a variable

    A var keeps track of the equation nodes it is attached to, and
    as variables and equations become solved/constrained, it keeps
    track of which equation nodes are reachable and not solved yet.

    Once a var is solved (aka assigned to an equation set that it is
    actually variable in), it keeps track of with equation set solves
    for it and which equation sets require it to be solved before they
    can solve for their variables.

    A var also tracks the actual value assigned to the variable.
    """

    __slots__ = (
        "eqns",  # equations that are available
        "all_eqns",  # all equations
        "solved_by",  # equation set that solves this
        "required_by",  # equation sets that require this to be solved
        "val",  # value of this variable
        "name",  # name of this variable
        "parent",  # containing parent (like a geom or constraint)
    )

    def __init__(self, name, val, parent=None):
        self.solved_by = None
        self.required_by = set()

        self.eqns = set()
        self.all_eqns = set()

        self.val = val
        self.name = name
        self.parent = parent

    def delete(self):
        """Delete this variable by deleting all equations it appears in"""
        all_eqns = self.all_eqns.copy()
        for eqn in all_eqns:
            eqn.delete()

    def reset(self):
        """Reset this variable by adding all eqns back to it"""
        self.eqns = self.all_eqns.copy()

        self.solved_by = None
        self.required_by = set()

    def remove(self, eqn):
        """Remove an equation from this variable"""
        self.eqns.discard(eqn)
        self.all_eqns.discard(eqn)

    def set_solved(self, eqn_set):
        """This variable is (or will be) solved by the given equation set"""
        self.solved_by = eqn_set

        for eqn in self.eqns:
            eqn.vars.discard(self)

        self.eqns -= eqn_set.eqns

    def is_constrained(self):
        """Is this var solved by a constrained equation set"""
        return self.solved_by is not None and self.solved_by.is_constrained()

    def __str__(self):
        return "Var:" + self.name + "=" + str(self.val)
    
x = Var('abc' + ".x", 10)
print(x)

import matplotlib.pyplot as plt  # TODO: add/remove this for profiling
class Point:
    def __init__(self, name, x=0.0, y=0.0):

        self.x = Var(name + ".x", x)
        self.y = Var(name + ".y", y)

        self.vars = [self.x, self.y]

    def plot(self, ax=None):
        ax = ax or plt.gca()
        ax.scatter(x=(self.x.val,), y=(self.y.val,))

class LineSegment:
    def __init__(self, name, x1=0.0, y1=0.0, x2=0.0, y2=0.0):
        self.p1 = Point(name + ".p1", x1, y1)
        self.p2 = Point(name + ".p2", x2, y2)
        self.vars = [self.p1.x, self.p1.y, self.p2.x, self.p2.y]

    def plot(self, ax=None):
        ax = ax or plt.gca()
        line = plt.Line2D(
            xdata=(self.p1.x.val, self.p2.x.val), ydata=(self.p1.y.val, self.p2.y.val)
        )
        ax.add_artist(line)
        self.p1.plot(ax)
        self.p2.plot(ax)

p0 = Point("p0", 0.0, 0.0)
p1 = Point("p1", 1.0, 1.0)
p2 = Point("p2", 2.0, 2.0)
p3 = Point("p3", 3.0, 3.0)
L1 = LineSegment("L1", 1.0, 1.0, 3.0, 3.0)
L1.plot()
p0.plot()
p1.plot()
p2.plot()
p3.plot()

plt.show()
print('')

# https://builtin.com/data-science/python-linked-list