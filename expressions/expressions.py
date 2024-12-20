"""Module implementing symbolic mathematical expressions."""
import numbers as n
from functools import singledispatch


class Expression:
    """Parent class for both terminals and operands in an expression."""

    def __init__(self, *operands):
        """Instantiate an expression."""
        self.operands = operands

    def __add__(self, other):
        """Define addition."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Add(self, other)

    def __radd__(self, other):
        """Define addition if called on non-expressions."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Add(other, self)

    def __sub__(self, other):
        """Define substraction."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Sub(self, other)

    def __rsub__(self, other):
        """Define substraction if called on non-expressions."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Sub(other, self)

    def __mul__(self, other):
        """Define multiplication."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Mul(self, other)

    def __rmul__(self, other):
        """Define multiplication if called on non-expressions."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Mul(other, self)

    def __truediv__(self, other):
        """Define division."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Div(self, other)

    def __rtruediv__(self, other):
        """Define division if called on non-expressions."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Div(other, self)

    def __pow__(self, other):
        """Define exponentiation."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Pow(self, other)

    def __rpow__(self, other):
        """Define exponentiation if called on non-expressions."""
        if isinstance(other, n.Number):
            other = Number(other)
        return Pow(other, self)


class Operator(Expression):
    """Subclass of Expression, for operators in an expression."""

    def __repr__(self):
        """Give canonical string representation."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Give human readable string representation."""
        b = [False, False]
        for i in range(2):
            if type(self.operands[i]).precedence < type(self).precedence:
                b[i] = True

        if b == [True, True]:
            return "(" + str(self.operands[0]) + ")" + " " + type(self).sym \
                  + " " + "(" + str(self.operands[1]) + ")"

        elif b == [True, False]:
            return "(" + str(self.operands[0]) + ")" + " " + type(self).sym \
                  + " " + str(self.operands[1])

        elif b == [False, True]:
            return str(self.operands[0]) + " " + type(self).sym \
                  + " " + "(" + str(self.operands[1]) + ")"

        else:
            return str(self.operands[0]) + " " + type(self).sym \
                  + " " + str(self.operands[1])


class Add(Operator):
    """Class for addition operation."""

    sym = "+"
    precedence = 0


class Sub(Operator):
    """Class for substraction operation."""

    sym = "-"
    precedence = 0


class Mul(Operator):
    """Class for multiplication operation."""

    sym = "*"
    precedence = 1


class Div(Operator):
    """Class for division operation."""

    sym = "/"
    precedence = 1


class Pow(Operator):
    """Class for exponenciation operation."""

    sym = "^"
    precedence = 2


class Terminal(Expression):
    """Subclass of Expression, for symbols and numbers in an expression."""

    def __init__(self, value):
        """Instanciate a terminal which needs to have a value."""
        self.value = value
        super().__init__()

    def __repr__(self):
        """Give canonical string representation."""
        return repr(self.value)

    def __str__(self):
        """Give human readable string representation."""
        return str(self.value)


class Number(Terminal):
    """Class for number terminal."""

    precedence = 3


class Symbol(Terminal):
    """Class for symbol terminal."""

    precedence = 3


def postvisitor(expr, fn, **kwarg):
    """Postvisit without recursion."""
    stack = []
    visited = dict()
    stack.append(expr)

    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            for uc in unvisited_children:
                stack.append(uc)
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands), **kwarg)

    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwarg):
    """Differentiate expressions."""
    raise NotImplementedError


@differentiate.register(Number)
def _(expr, *o, **kwarg):
    return 0


@differentiate.register(Symbol)
def _(expr, var, *o, **kwarg):
    if expr.value == var:
        return 1
    else:
        return 0


@differentiate.register(Add)
def _(expr, *o, **kwarg):
    return o[0] + o[1]


@differentiate.register(Mul)
def _(expr, *o, **kwarg):
    return o[0] * expr.operands[1] + o[1] * expr.operands[0]


@differentiate.register(Div)
def _(expr, *o, **kwarg):
    return (o[0] * expr.operands[1] - o[1] * expr.operands[0]) \
        / (expr.operands[1])**2


@differentiate.register(Pow)
def _(expr, *o, **kwarg):
    return o[0] * expr.operands[1] * expr.operands[0] ** (expr.operands[1] - 1)
