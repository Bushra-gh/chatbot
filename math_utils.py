import re

def solve_math_expression(expr):
    try:
        match = re.search(r"(-?\d+(?:\s*[\+\-\*/]\s*-?\d+)+)", expr)
        if match:
            math_expr = match.group(1)
            result = eval(math_expr)
            return f"That's {result}."
        else:
            return "I couldn't find a math expression to solve."
    except:
        return "I couldn't solve that math expression."

