import re
import doctest
import hashlib

__version__ = '0.001'

# TODO:
#  - Caching of parse trees of files (will require timestamp checking)
#  - File directories?  (current, templates, passed in?)
#  - Given an email, return a gravatar
#  - {% include "file" with var0 = a, var1 = b %}
#  - {% exec .... %}
#  - pretty=True (automatic prettification of html - i.e. call someone else's prettifier)
#  - {% iif .... then .... else .... %}
#  - support recursion


# Abstract Node Class:
class Node(object):
    def render(self, variables):
        raise NotImplementedError()

# Node for plain text:
class TextNode(Node):
    def __init__(self, text):
        self.text = text

    # Simply render the text:
    def render(self, variables):
        return self.text

# Node for holding groups of nodes:
class GroupNode(Node):
    def __init__(self, sub_nodes):
        self.sub_nodes = sub_nodes

    # Render each child node one after another:
    def render(self, variables):
        return ''.join(node.render(variables) for node in self.sub_nodes)

# Node for holding python code to evaluate:
class PythonNode(Node):
    def __init__(self, code):
        self.code = code

    # Evaluate and stringify the expression:
    def render(self, variables):
        return str(eval(self.code, {}, variables))

# Node for handling if and else blocks:
class IfNode(Node):
    def __init__(self, expr, istrue, isfalse):
        self.expr = expr
        self.istrue = istrue
        self.isfalse = isfalse

    # Evaluate the precondition, and render the appropriate child node:
    def render(self, variables):
        if eval(self.expr, {}, variables):
            return self.istrue.render(variables)
        else:
            return self.isfalse.render(variables)

# Node for generating gravatar image links
class GravatarNode(Node):
    def __init__(self, email):
        self.email = email

    def render(self, variables):
        hashed = hashlib.md5(self.email.lower().strip().encode('ascii')).hexdigest()
        return 'http://www.gravatar.com/avatar/' + hashed


# Node for handling for loops:
class ForNode(Node):
    def __init__(self, variables, expr, enclosed):
        self.variables = variables
        self.expr = expr
        self.enclosed = enclosed

    # Loop over the iterable, rendering the child nodes:
    def render(self, variables):
        variables['___iterator'] = iter(eval(self.expr, {}, variables))
        output = ''
        while True:
            try:
                exec(self.variables + ' = ' + 'next(___iterator)', {}, variables)
            except StopIteration:
                break
            else:
                output += self.enclosed.render(variables)
        del variables['___iterator']
        return output


# Abstract class for parsing exceptions:
class TemplateException(Exception):
    pass

# Exception raised when if/else/endif or for/endfor statements are not in correct blocks:
class NoMatchingEndToken(TemplateException):
    pass



# 'Lex' the text into blocks for later parsing:
def lex(text):

    # List of tokens:
    tokens = []

    ###  Token Descriptions: ###
    #
    # Below, each token is specified as an identifier
    # followed by a regex string that matches it.
    #
    # Tokens are tried in the order they are listed,
    # and any capturing groups (bracketed parts of the
    # regex) are returned by the function.
    #
    ############################

    # Hackily get a list of labels and regex objects that match them:
    token_reg = [(label, re.compile(regex)) for label, regex in (l.split() for l in r'''

    eval {{(.*?)}}
    exec {%\s*exec\s(.*?)%}

    if {%\s*if\s(.*?)%}
    else {%\s*else\s*%}
    endif {%\s*endif\s*%}

    for {%\s*for\s(.*?)\s*in\s*(.*?)\s*%}
    endfor {%\s*endfor\s*%}

    include {%\s*include\s\"(.*?)\"\s*%}
    include_remap {%\s*include\s(.*?)\swith(\s.*?\sas\s.*?)+%}

    comment {#.*?#}

    gravatar {%\s*gravatar\s(.*?)%}

    '''.split('\n') if l.strip())]


    # For each relevant block:
    for block in re.split(r'({{.*?}}|{%.*?%}|{#.*?#})', text):

        # Try matching each of the tokens:
        label = None
        for token, regex in token_reg:
            match = regex.match(block)
            if match:
                # If there is a match, extract the matched text into expr or into a tuple if multiple capturing groups:
                label = token
                expr = match.groups()
                if len(expr) == 1:
                    expr = expr[0]
                elif len(expr) == 0:
                    expr = None
                break

        # If nothing was matched, mark the block as plain-text:
        if label is None:
            label = 'text'
            expr = block

        tokens.append((label, expr))

    return tokens


# Reads a file and returns a parse tree for the file:  (TODO: Caching parse trees.)
def parse_file(filename):
    with open(filename) as f:
        text = f.read()
    return parse(text)

# Lexes the template string and runs the parser, returning a parse tree:
def parse(template):
    return parse_template(iter(lex(template)))

# Recursive template parser, returning a parse tree:
def parse_template(iterator, last=None):

    current_nodes = []

    while True:
        try:
            tok_type, tok_text = next(iterator)
        except StopIteration:
            break

        if tok_type == 'text':
            current_nodes.append(TextNode(tok_text))

        elif tok_type == 'eval':
            current_nodes.append(PythonNode(tok_text))

        elif tok_type == 'else':
            if last == 'if':
                return (GroupNode(current_nodes), parse_template(iterator, 'else')[0])
            else:
                raise NoMatchingEndToken('"else" without "if"')

        elif tok_type == 'endif':
            if last in ('if', 'else'):
                return (GroupNode(current_nodes), TextNode(''))
            else:
                raise NoMatchingEndToken('"endif" without "if"')

        elif tok_type == 'endfor':
            if last == 'for':
                return GroupNode(current_nodes)
            else:
                raise NoMatchingEndToken('endfor without for')

        elif tok_type == 'if':
            istrue, isfalse = parse_template(iterator, 'if')
            current_nodes.append(IfNode(tok_text, istrue, isfalse))

        elif tok_type == 'for':
            variables, iterable = tok_text
            current_nodes.append(ForNode(variables, iterable, parse_template(iterator, 'for')))

        elif tok_type == 'include':
            current_nodes.append(parse_file(tok_text))

        elif tok_type == 'comment':
            pass # Ignore

        # special tokens
        elif tok_type == 'gravatar':
            current_nodes.append(GravatarNode(tok_text))

    return GroupNode(current_nodes)


def render(template, variables={}):
    """
    Renders a template string as text
    Returns rendered template

    >>> render("{{string}}", variables={'string': 'this is a string'})
    'this is a string'
    """
    tree = parse(template)

    return tree.render(variables)


def render_file(filename, variables={}):
    """
    call with the relative path of the template as filename, and the list of variables as variables
    """
    return parse_file(filename).render(variables)


def main():
    doctest.testmod()
    # Doctest is currently broken in python32... (one character fix though)


if __name__ == '__main__':
    main()

    # variables = {
    #     'title': 'world',
    #     'heh': 'heh',
    #     'python': 'bah'}

    # print(render_file('simple_test.html', {'python': 'woo', 'nope': "hello"}))
    # tree = parse(open('simple_test.html').read())
