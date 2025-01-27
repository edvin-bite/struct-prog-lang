"""
    simple_expresion = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    arithmetic_expression = term { "+"|"-" term }
    expression = arithmetic_expression
"""