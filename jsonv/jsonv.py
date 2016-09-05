""" JSONv Python Library """
import antlr4
import json
from JSONvLexer import JSONvLexer
from JSONvParser import JSONvParser


class JSONvPythonVisitor(antlr4.ParseTreeVisitor):

    def __init__(self, bindings):
        self._bindings = bindings

    def visitJsonObject(self, ctx):
        """ The JSON Object visitor needs to return a python dict containing
        the key/pairs that exist as children """
        d = JVDict()
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
        return JVList([self.visit(child) for child in children])

    def visitUnbound(self, ctx):
        var = str(ctx.UNBOUND())
        # If the var isn't in the bindings, raise an exception
        if var not in self._bindings:
            return JVVariable(var, bound=False)
        else:
            return JVVariable(var, bound=True, value=self._bindings[var])

    def visitTrue(self, ctx):
        return True

    def visitFalse(self, ctx):
        return False

    def visitNull(self, ctx):
        return None

    def visitString(self, ctx):
        return json.loads(str(ctx.STRING()))

    def visitNumber(self, ctx):
        num_str = str(ctx.NUMBER())
        try:
            return int(num_str)
        except ValueError:
            return float(num_str)


class JVObject(object):

    def _dumps(self):
        raise NotImplementedError()

    def bind(self):
        raise NotImplementedError()


class JVVariable(JVObject):

    def __init__(self, name, bound=False, value=None):
        self.name = name
        self.bound = bound
        self.value = None

    def bind(self, bindings):
        if self.name in bindings:
            self.bound = True
            self.value = bindings[self.name]

    def _dumps(self):
        if not self.bound:
            # Return the variable name if we're not bound
            return self.name
        else:
            # Else the JSON representation of the type
            return json.dumps(self.value)


class JVDict(JVObject, dict):

    def bind(self, bindings):
        for v in self.values():
            if isinstance(v, JVObject):
                v.bind(bindings)

    @property
    def bound(self):
        return not any([isinstance(v, JVObject) and not v.bound for v in self.values()])

    def _dumps(self):
        return "{" + ", ".join([
            json.dumps(k) + ": " + (dumps(v) if isinstance(v, JVObject) else json.dumps(v))
            for k, v in self.iteritems()
        ]) + "}"


class JVList(JVObject, list):

    def bind(self, bindings):
        for v in self:
            if isinstance(v, JVObject):
                v.bind(bindings)

    @property
    def bound(self):
        return not any([isinstance(v, JVObject) and not v.bound for v in self])

    def _dumps(self):
        return "[" + ", ".join([
            dumps(v) if isinstance(v, JVObject) else json.dumps(v)
            for v in self
        ]) + "]"


def dumps(jvo):
    if isinstance(jvo, JVObject):
        return jvo._dumps()
    else:
        return str(jvo)


def from_dict(d):
    """ Return a JSONv object from a Python dictionary """
    return JVDict(d)


def loads(jsonv_str, bindings=None):
    bindings = bindings or {}
    f = antlr4.InputStream(jsonv_str)
    lexer = JSONvLexer(f)
    stream = antlr4.CommonTokenStream(lexer)
    parser = JSONvParser(stream)
    return JSONvPythonVisitor(bindings).visit(parser.jsonv())


def load(file_obj):
    # Antlr FileStream takes a filename and just loads the whole file
    # anyway...
    return loads(file_obj.read())
