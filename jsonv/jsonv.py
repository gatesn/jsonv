""" JSONv Python Library """
import antlr4
from JSONvLexer import JSONvLexer
from JSONvParser import JSONvParser


class MissingBindingException(Exception):
    pass


class JSONvPythonVisitor(antlr4.ParseTreeVisitor):

    def __init__(self, bindings):
        self._bindings = bindings

    def visitJsonObject(self, ctx):
        """ The JSON Object visitor needs to return a python dict containing
        the key/pairs that exist as children """
        d = dict()
        for child in ctx.getChildren():
            c = self.visit(child)
            if isinstance(c, dict):
                d.update(c)
        return d

    def visitPair(self, ctx):
        """ Return a dict containing a single key/pair """
        return {self.visit(ctx.string()): self.visit(ctx.value())}

    def visitJsonArray(self, ctx):
        """ Return a python array containing elements """
        # Filter out any terminal nodes (e.g. '[' and ',')
        children = [
            c for c in ctx.getChildren()
            if not isinstance(c, antlr4.TerminalNode)
        ]
        return [self.visit(child) for child in children]

    def visitUnbound(self, ctx):
        var = str(ctx.UNBOUND())
        # If the var isn't in the bindings, raise an exception
        if var not in self._bindings:
            raise MissingBindingException(var)
        return self._bindings[var]

    def visitTrue(self, ctx):
        return True

    def visitFalse(self, ctx):
        return False

    def visitNull(self, ctx):
        return None

    def visitString(self, ctx):
        # We strip the quotation  marks off beginning and end
        return str(ctx.STRING())[1:-1]

    def visitNumber(self, ctx):
        num_str = str(ctx.NUMBER())
        try:
            return int(num_str)
        except ValueError:
            return float(num_str)


class JSONv(object):

    def __init__(self, stream):
        lexer = JSONvLexer(stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = JSONvParser(stream)
        self._tree = parser.jsonv()

    def bind(self, bindings):
        """ Binds the given dictionary of values returning an object """
        visitor = JSONvPythonVisitor(bindings)
        return visitor.visit(self._tree)


def loads(jsonv_str):
    f = antlr4.InputStream(jsonv_str)
    return JSONv(f)


def load(filename):
    f = antlr4.FileStream(filename)
    return JSONv(f)
