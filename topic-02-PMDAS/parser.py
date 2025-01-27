"""


accept a string of tokens, return all ASI expressed as stack of {dictionaries(?)}
"""
"""
    simple_expresion = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    arithmetic_expression = term { "+"|"-" term }
    expression = arithmetic_expression
"""
""" personal
rules:
1: e = ae
2: ae = t{+/- t}
3: t = f{*// f}
4: f = se
5: se = <number> | "(" e ")" | "-" se

line : rule numbers
"2": 5
"3+2": 2,3,3,4,4,5,5
    t "+" t
    f "t" f 
    se + se
    n  +  n

forms a tree; makes an Abstract Syntax Tree.
define ASTs as a Python Dictionary.
ex.:
{
    tag: "+"
    left: {
        tag: "number"
        value: 3
    }
    right:{...}
}

looking at A token, "based on this, what needs to happen?" if can be done as simply as this,
  it becomes a general decent parser. 
  causes probmles with end of line options like !! at the end
  saying if variable should be a file or variable.
  however we are writing a recursive decent parser.
"""