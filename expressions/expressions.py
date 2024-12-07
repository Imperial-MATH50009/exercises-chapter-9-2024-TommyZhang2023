"""Module implementing symbolic mathematical expressions."""
import numbers as n


class Expression:
    """Parent class for both terminals and operands in an expression."""

    def __init__(self, *operands):
        """Instantiate an expression."""
        self.operands = operands

    def __add__(self, other):
        """Define addition between expressions."""
        if isinstance(self, n.Number):
            self = Number(self)
        if isinstance(other, n.Number):
            other = Number(other)
        return Add(self, other)

    def __sub__(self, other):
        """Define substraction between expressions."""
        if isinstance(self, n.Number):
            self = Number(self)
        if isinstance(other, n.Number):
            other = Number(other)
        return Sub(self, other)

    def __mul__(self, other):
        """Define multiplication between expressions."""
        if isinstance(self, n.Number):
            self = Number(self)
        if isinstance(other, n.Number):
            other = Number(other)
        return Mul(self, other)

    def __truediv__(self, other):
        """Define division between expressions."""
        if isinstance(self, n.Number):
            self = Number(self)
        if isinstance(other, n.Number):
            other = Number(other)
        return Div(self, other)

    def __pow__(self, other):
        """Define exponentiation between expressions."""
        if isinstance(self, n.Number):
            self = Number(self)
        if isinstance(other, n.Number):
            other = Number(other)
        return Pow(self, other)


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
            return "(" + str(self.operands[0]) + ")" + type(self).sym \
                  + "(" + str(self.operands[1]) + ")"

        elif b == [True, False]:
            return "(" + str(self.operands[0]) + ")" + type(self).sym \
                  + str(self.operands[1])

        elif b == [False, True]:
            return str(self.operands[0]) + type(self).sym \
                  + "(" + str(self.operands[1]) + ")"

        else:
            return str(self.operands[0]) + type(self).sym \
                  + str(self.operands[1])


class Add(Operator):
    """Class for addition operation."""

    sym = "+"
    precendence = 0


class Sub(Operator):
    """Class for substraction operation."""

    sym = "-"
    precendence = 0


class Mul(Operator):
    """Class for multiplication operation."""

    sym = "*"
    precendence = 1


class Div(Operator):
    """Class for division operation."""

    sym = "/"
    precendence = 1


class Pow(Operator):
    """Class for exponenciation operation."""

    sym = "^"
    precendence = 2


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