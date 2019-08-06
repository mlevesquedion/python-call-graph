import collections
import ast


class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.callees = collections.defaultdict(list)
        self.visiting_def = None

    def visit_FunctionDef(self, node):
        self.visiting_def = node.name
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Name):
            callee_name = func.id
        elif isinstance(func, ast.Attribute):
            callee_name = func.attr
        else:
            raise ValueError(f"I don't know how to handle: {node}")

        self.callees[self.visiting_def].append(callee_name)
        self.generic_visit(node)

    def call_graph(self):
        return dict(self.callees)
