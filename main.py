import ast
import call_graph


def main():
    with open("call_graph.py", "r") as source:
        tree = ast.parse(source.read())
    visitor = call_graph.CallGraphVisitor()
    visitor.visit(tree)
    print(visitor.call_graph())


if __name__ == '__main__':
    main()
