
import ast
import operator
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}
def calculate_node(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in operators:
        left = calculate_node(node.left)
        right = calculate_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Power is too large")
        return operators[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = calculate_node(node.operand)
        if isinstance(node.op, ast.USub):
            return -value
        return value
    raise ValueError("Invalid expression")
def safe_calculate(expression):
    tree = ast.parse(expression, mode="eval")
    return calculate_node(tree.body)