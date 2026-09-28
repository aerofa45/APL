"""Lexically nested symbol tables used by the Emerald interpreter."""


class EmeraldRuntimeError(Exception):
    def __init__(self, message, node=None):
        location = f" at line {node.line}, column {node.column}" if node else ""
        super().__init__(f"Runtime error{location}: {message}")


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def define(self, name, value, node=None):
        if name in self.values:
            raise EmeraldRuntimeError(f"'{name}' is already declared in this scope", node)
        self.values[name] = value

    def resolve(self, name, node=None):
        scope = self
        while scope is not None:
            if name in scope.values:
                return scope
            scope = scope.parent
        raise EmeraldRuntimeError(f"undefined variable '{name}'", node)

    def get(self, name, node=None):
        return self.resolve(name, node).values[name]

    def assign(self, name, value, node=None):
        self.resolve(name, node).values[name] = value
