import ast
from pytest import mark
import call_graph


@mark.parametrize(
    ['source_code', 'expected'],
    [
        ('', {}),
        ('''\
def foo():
    pass''',
         {}),
        ('''\
def bar():
    pass

def foo():
    bar()''',
         {'foo': ['bar']}),
        ('''\
def bar():
    pass

def foo():
    bar()

def baz():
    foo()
    ''', {'foo': ['bar'], 'baz': ['foo']}),
        ('''\
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
''', {'__init__': ['defaultdict'], 'visit_FunctionDef': ['generic_visit'], 'visit_Call': ['isinstance', 'isinstance', 'ValueError', 'append', 'generic_visit'], 'call_graph': ['dict']}
        )
    ],
)
def test_given_code_produces_correct_graph(source_code, expected):
    visitor = call_graph.CallGraphVisitor()
    tree = ast.parse(source_code)
    visitor.visit(tree)
    assert visitor.call_graph() == expected
