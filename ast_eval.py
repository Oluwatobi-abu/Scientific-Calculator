import ast
import math
from engine.evaluator import Evaluator


ALLOWED_CONSTS = {
    "pi": math.pi,
    "e": math.e,
}


class ASTEvaluator(Evaluator):
    def __init__(self, engine=None):
        self.engine = engine
    def evaluate(self, expr, **vars):
        expr = expr.replace("^", "**")
        self.vars = vars
        node = ast.parse(expr, mode="eval")
        return self._eval(node.body)

    def _eval(self, node):
        # Binary operations: + - * / **
        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right

            raise ValueError("Unsupported operator")

        # Unary operations: -x
        if isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
            return operand

        # Numbers
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value

        # Constants like pi, e
        if isinstance(node, ast.Name):
            if node.id in self.vars:
                return self.vars[node.id]

            if node.id in ALLOWED_CONSTS:
                return ALLOWED_CONSTS[node.id]

            raise ValueError(f"Unknown variable '{node.id}'")

        # Function calls like sin(x)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function call")

            func_name = node.func.id
            args = [self._eval(arg) for arg in node.args]

            if self.engine:
                funcs = self.engine.allowed_names()
                if func_name in funcs:
                    return funcs[func_name](*args)

            raise ValueError(f"Function '{func_name}' not allowed")
    
        #remove later
        if __name__ == "__main__":
            e = ASTEvaluator()
            print(e.evaluate("x", x=5))

