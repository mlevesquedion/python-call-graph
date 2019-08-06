import ast
import sys

import graphviz

import call_graph


def main():
    with open(sys.argv[1], "r") as source:
        tree = ast.parse(source.read())
    visitor = call_graph.CallGraphVisitor()
    visitor.visit(tree)
    dot = graphviz.Digraph(name='call_graph', format='pdf')
    dot.edges([(node, child) for node, children in visitor.call_graph().items()
               for child in children])
    dot.render()


if __name__ == '__main__':
    main()
