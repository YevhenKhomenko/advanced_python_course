import ast
import math


class AstCalculator(ast.NodeTransformer):

    def __init__(self):
        self._pi = math.pi
        self._e = math.e

    def visit_Name(self, node: ast.Name):
        if node.id == 'pi':
            result = ast.Constant(value=self._pi)
            return ast.copy_location(result, node)

        elif node.id == 'e':
            result = ast.Constant(value=self._e)
            return ast.copy_location(result, node)

        else:
            raise SyntaxError("Unsupported expression.")

    def visit_BinOp(self, node: ast.BinOp):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            if isinstance(node.op, ast.Add):
                result = ast.Constant(value=node.left.value + node.right.value)
                return ast.copy_location(result, node)

            elif isinstance(node.op, ast.Sub):
                result = ast.Constant(value=node.left.value - node.right.value)
                return ast.copy_location(result, node)

            elif isinstance(node.op, ast.Mult):
                result = ast.Constant(value=node.left.value * node.right.value)
                return ast.copy_location(result, node)

            elif isinstance(node.op, ast.Div):
                result = ast.Constant(value=node.left.value / node.right.value)
                return ast.copy_location(result, node)

            elif isinstance(node.op, ast.FloorDiv):
                result = ast.Constant(value=node.left.value // node.right.value)
                return ast.copy_location(result, node)

            elif isinstance(node.op, ast.Mod):
                result = ast.Constant(value=node.left.value % node.right.value)
                return ast.copy_location(result, node)

            elif isinstance(node.op, ast.Pow):
                result = ast.Constant(value=node.left.value ** node.right.value)
                return ast.copy_location(result, node)

            else:
                raise SyntaxError("Unsupported operator.")


class AstResultVisitor(ast.NodeVisitor):

    def __init__(self):
        self._result = None

    @property
    def result(self):
        res = self._result
        self._result = None
        return res

    def visit_Expr(self, node: ast.Expr):
        if isinstance(node.value, ast.Constant):
            self._result = node.value.value

        else:
            raise SyntaxError("Wrong syntax.")


def main():
    calc = AstCalculator()
    res_visitor = AstResultVisitor()
    while True:
        try:
            expr = input('Enter expression(ctrl+c to exit): ')
            tree = ast.parse(expr)
            tree = calc.visit(tree)
            print('Result tree: ', ast.dump(tree))
            res_visitor.visit(tree)
            print('Result: ', res_visitor.result)

        except KeyboardInterrupt:
            break

        except SyntaxError:
            print('Wrong syntax. Try again.')
            pass


if __name__ == '__main__':
    main()
