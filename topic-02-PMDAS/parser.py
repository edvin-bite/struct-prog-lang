from tokenizer import tokenize
"""
parser.py -- implement parser for simple expressions

accept a string of tokens, return all ASI expressed as stack of dictionaries
"""
"""
    simple_expresion = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    arithmetic_expression = term { "+"|"-" term }
    expression = arithmetic_expression
    statement = expression
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

"""
    factor = <number> | "(" expresion ")"
    term = factor { "*"|"/" factor }
    expression = term { "+"|"-" term }
"""

def parse_factor(tokens):
    """
    factor = <number> | "(" expresion ")"
    """
    token = tokens[0]
    if token["tag"] == "number":
        return {
            "tag":"number",
            "value": token["value"]
        }, tokens[1:]
    if token["tag"] == "(":
        #tokens = tokens[1:]
        ast, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")"
        #tokens = tokens[1:]
        return ast, tokens[1:]
    raise Exception(f"Unexpected token '{token['tag']}' at position {token['position']}.")

def test_parse_factor():
    """
    factor = <number>
    """
    for s in ["1","22","333"]:
        #tokens = tokenize("1")
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        assert ast == {'tag':'number', 'value':int(s)}
        assert tokens[0]['tag']==None
        #print(ast)
    for s in ["(1)", "(22)"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        s_n = s.replace("(","").replace(")","")
        #s_n = s[1:-1]
        assert ast == {'tag':'number', 'value':int(s_n)}
        assert tokens[0]['tag']==None
    tokens = tokenize("(2+3)")
    ast, tokens = parse_factor(tokens)
    s_n = s.replace("(","").replace(")","")

    #exit(0)
    print("done test parse factor.")

def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*","/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag":tag, "left":node, "right":right_node}
    return node, tokens

def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_term(tokens)
        assert ast=={'tag':'number', 'value':int(s)}
        assert tokens[0]['tag']==None
    tokens = tokenize("2*4/6")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '/', 'left': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {   'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 6}}
    #print(ast)
    print("done test parse term.")
    #exit(0)

def parse_expression(tokens):
    """
    arithmetic_expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+","-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag":tag, "left":node, "right":right_node}
    return node, tokens



def test_parse_expression():
    """
    arithmetic_expression = term { "+"|"-" term }
    """
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_expression(tokens)
        assert ast=={'tag':'number', 'value':int(s)}
        assert tokens[0]['tag']==None
    tokens = tokenize("2*4/6")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '/', 'left': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {   'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 6}}
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_expression(tokens)
    #print(ast)
    print("done test parse arithetic expression.")
    #exit(0)

def parse_statement(tokens):
    """
    statement = expression
    """
    # if consume non terminal, use that non terminal's rule to consume it
    ast, tokens = parse_expression(tokens)
    return ast, token

def test_parse_statement():
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_expression(tokens)
        assert ast=={'tag':'number', 'value':int(s)}
        assert tokens[0]['tag']==None
    tokens = tokenize("2*4/6")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '/', 'left': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {   'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 6}}
    tokens = tokenize("1+2*4")
    ast, tokens = parse_expression(tokens)
    print(ast)
    print("done test parse arithetic statement.")
    exit(0)

def parse(tokens):
    return parse_expression(tokens)[0]

if __name__ == "__main__":
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse_statement()