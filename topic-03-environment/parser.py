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
    assignment = expression [ "=" expression ]
    program = [ statement { ";" statement } ]
"""

def parse_factor(tokens):
    """
    factor = <number> | <identifier> | "(" expresion ")"
    """
    token = tokens[0]
    if token["tag"] == "number":
        return {
            "tag":"number",
            "value": token["value"]
        }, tokens[1:]
    if token["tag"] == "identifier":
        return {
            "tag":"identifier",
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
    print("testing parse_factor()")
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
    #s_n = s.replace("(","").replace(")","")
    assert ast == {'tag': '+', 'left': {'tag':'number', 'value':2}, 'right': {'tag':'number' , 'value':3}}
    tokens = tokenize("x")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag':'identifier','value':'x'}
    tokens = tokenize("(x+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {
        'tag': '+', 
        'left': {'tag':'identifier', 'value':"x"}, 
        'right': {'tag':'number' , 'value':3}
    }
    #exit(0)

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
    print("testing parse_term()")
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
    tokens = tokenize("2*4/6") # is error if fails here, if not ignore.
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
    statment = <print> expression | expression
    """
    if tokens[0]["tag"] == "print": # adding an operator
        expr_ast, tokens = parse_expression(tokens[1:])
        ast = {
            'tag':'print',
            'value': expr_ast
        }
    else:
        ast, tokens = parse_assignment_statement(tokens)#(tokens[1:]) | no cutting the tokens
    return ast, tokens

def test_parse_statement():
    """
    statement = expression
    statment = <print> expression | expression
    """
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

    tokens = tokenize("print 1*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': 'print', 'value': {'tag': '*', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': 'number', 'value': 4}}}
    #print(ast)
    print("done test parse arithetic statement.")
    #exit(0)

def parse_assignment_statement(tokens):
    """
    assignment_statement = expression [ "=" expression ] ;
    """
    target, tokens = parse_expression(tokens)
    if tokens[0]["tag"] == "=":
        tokens = tokens[1:]
        value, tokens = parse_expression(tokens)
        return {"tag": "assign", "target": target, "value": value}, tokens
    return target,tokens

def test_parse_assignment_statement():
    """
    
    """
    print("test parse_assignment_statement...")
    ast, tokens = parse_assignment_statement(tokenize("i=2"))
    print(ast)

def parse(tokens):
    ast, tokens = parse_statement(tokens)
    return ast

if __name__ == "__main__":
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse_statement()
    test_parse_assignment_statement()
    print("done.")
