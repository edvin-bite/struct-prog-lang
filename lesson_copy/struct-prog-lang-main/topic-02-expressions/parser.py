from tokenizer import tokenize

"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""

"""
    factor = <number> | <identifier> | "(" expression ")"
    term = factor { "*"|"/" factor }
    expression = term { "+"|"-" term }
    statement = <print> expression | expression
"""

def parse_factor(tokens):
    """
    factor = <number> | "(" expression ")"
    """
    token = tokens[0]
    if token["tag"] == "number": # given a number, the factor is compleate and passed back apended.
        return {
            "tag":"number",
            "value": token["value"]
        }, tokens[1:]
    if token["tag"] == "(": # a parentises causes a new expression and resets the parse order within the parentheses.
        ast, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")"
        return ast, tokens[1:]
    raise Exception(f"Unexpected token '{token['tag']}' at position {token['position']}.")

def test_parse_factor():
    """
    factor = <number> | <identifier> | "(" expression ")"
    """
    print("testing parse_factor()")
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        assert ast=={'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None 
    for s in ["(1)","(22)"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        s_n = s.replace("(","").replace(")","")
        assert ast=={'tag': 'number', 'value': int(s_n)}
        assert tokens[0]['tag'] == None 
    tokens = tokenize("(2+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}
    tokens = tokenize("(4-(3+6)/2)")
    ast, tokens = parse_factor(tokens)
    assert ast == {
        'tag': '-', 
        'left': {
            'tag': 'number', 
            'value': 4
        }, 
        'right': {
            'tag': '/', 
            'left': {
                'tag': '+', 
                'left': {
                    'tag': 'number', 
                    'value': 3
                }, 
                'right': {
                    'tag': 'number', 
                    'value': 6
                }
            }, 
            'right': {
                'tag': 'number', 
                'value': 2
            }
        }
    }

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
# order is in parse_expression() -> parse_term() -> parse_factor(), each on diffrent levels of priority
# expression is first, with tree structure, it is evaluated last, finalized when term returns.

def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term()")
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_term(tokens)
        assert ast=={'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None 
    tokens = tokenize("2*4")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}
    tokens = tokenize("2*4/6")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '/', 'left': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 6}}
    tokens = tokenize("(1+1)*1") # "+" fails as it is not in factor's scope
    ast, tokens = parse_term(tokens)
    assert ast == { # tree build by hand
        'tag': '*',
        'left': {
            'tag': '+',
            'left': {
                'tag': 'number',
                'value': 1
            },
            'right': {
                'tag':'number',
                'value': 1
            }
        },
        'right': {
            'tag': 'number',
            'value': 1
        }
    }

def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+","-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag":tag, "left":node, "right":right_node}

    return node, tokens

def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression()")
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_expression(tokens)
        assert ast=={'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None 
    tokens = tokenize("2*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}
    tokens = tokenize("1+2*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}
    # prove PMDAS by writing reverse
    tokens = tokenize("(1-2+3/4*5)+0")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'tag': '+', 
        'left': {
            'tag': '+', 
            'left': {
                'tag': '-', # - evaluated first, as priority left to right
                'left': {
                    'tag': 'number', 
                    'value': 1
                }, 
                'right': {
                    'tag': 'number', 
                    'value': 2
                }
            }, 
            'right': { # ...+(evaluated first) MD
                'tag': '*', 
                'left': {
                    'tag': '/', 
                    'left': {
                        'tag': 'number', 
                        'value': 3
                    }, 
                    'right': {
                        'tag': 'number', 
                        'value': 4
                    }
                }, 
                'right': {
                    'tag': 'number', 
                    'value': 5
                }
            }
        }, 
        'right': {
            'tag': 'number', 
            'value': 0
        } # P done first, despite the "+"
    }

def parse_statement(tokens):
    """
    statement = <print> expression | expression
    """
    if tokens[0]["tag"] == "print":
        value_ast, tokens = parse_expression(tokens[1:])
        ast = {
            'tag':'print',
            'value': value_ast
        }

    else:
        ast, tokens = parse_expression(tokens)
    return ast, tokens

def test_parse_statement():
    """
    statement = <print> expression | expression
    """
    print("testing parse_statement()")
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}
    tokens = tokenize("print 2*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': 'print', 'value': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}



def parse(tokens):
    ast, tokens = parse_statement(tokens)
    return ast

if __name__ == "__main__":
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse_statement()
    print("done.")
