import re
import os
import hashlib

__version__ = '0.05'

# TODO:
#  - pretty=True (automatic prettification of html - i.e. call someone else's prettifier)


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

	def __repr__(self):
		return 'TextNode: {}'.format(self.text)

# Node for holding groups of nodes:
class GroupNode(Node):
	def __init__(self, sub_nodes):
		self.sub_nodes = sub_nodes

	# Adds a node to this node's children:
	def add(self, node):
		self.sub_nodes.append(node)

	# Render each child node one after another:
	def render(self, variables):
		return ''.join(node.render(variables) for node in self.sub_nodes)

	def __repr__(self):
		return 'GroupNode (\n' + '\n'.join(repr(child) for child in self.sub_nodes) + '\n)'

# Node for holding python code to evaluate:
class PythonNode(Node):
	def __init__(self, code):
		self.code = code

	# Evaluate and stringify the expression:
	def render(self, variables):
		return str(eval(self.code, {}, variables))

	def __repr__(self):
		return 'PythonNode: {}'.format(self.code)

# Node for holding python code to execute:
class ExecNode(Node):
	def __init__(self, code):
		self.code = code

	# Execute the expression and return nothing:
	def render(self, variables):
		exec(self.code, {}, variables)
		return ''

	def __repr__(self):
		return 'ExecNode: {}'.format(self.code)

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

	def __repr__(self):
		return 'IfNode (\n{}\n) else (\n{}\n}'.format(repr(self.istrue), repr(self.isfalse))

# Node for generating gravatar image links
class GravatarNode(Node):
	def __init__(self, email):
		self.email = email

	def render(self, variables):
		hashed = hashlib.md5(str(eval(self.email)).lower().strip().encode('ascii')).hexdigest()
		return 'http://www.gravatar.com/avatar/' + hashed

	def __repr__(self):
		return 'GravatarNode: {}'.format(self.email)


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

# Node for remapping variables when including files:
class IncludeNode(Node):
	def __init__(self, child, remappings):
		self.child = child
		self.remap = [r.strip().split('=') for r in remappings if r.strip()]

	# Remap the variables, and render the included file:
	def render(self, variables):
		new_vars = dict((variable.strip(), eval(expression, {}, variables)) for variable, expression in self.remap)
		return self.child.render(new_vars)


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

	iif_else {%\s*iif\s(.*?)\s%then%\s(.*?)\s%else%\s(.*?)%}
	iif {%\s*iif\s(.*?)\s%then%\s(.*?)\s%}

	for {%\s*for\s(.*?)\s*in\s*(.*?)\s*%}
	endfor {%\s*endfor\s*%}

	include_remap {%\s*include\s\"(.*?)\"\swith\s(.*?=.*?(?:;.*?=.*?)*?)%}
	include {%\s*include\s\"(.*?)\"\s*%}

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
	if not os.path.exists(filename):
		old_name = filename
		filename = os.path.join('templates', filename)
		if not os.path.exists(filename):
			raise IOError('The file "{}" could not be found in the root directory or in the templates folder.'.format(old_name))

	with open(filename) as f:
		text = f.read()

	return parse(text)

# Lexes the template string and runs the parser, returning a parse tree:
def parse(template):
	return parse_template(iter(lex(template)), template=template)

# Recursive template parser, returning a parse tree:
def parse_template(iterator, last=None, template=None):
	
	if template is not None:
		parse_template.cache = parse_template.__dict__.get('cache', dict())
		if template in parse_template.cache:
			return parse_template.cache[template]
	
	# The grouping node to return as a result:
	result = GroupNode([])
	if template:
		parse_template.cache[template] = result

	while True:
		# Consume tokens until there are none left:
		try:
			tok_type, parameters = next(iterator)
		except StopIteration:
			break

		# If text, simply add a TextNode:
		if tok_type == 'text':
			result.add(TextNode(parameters))

		# If an expression, add a PythonNode:
		elif tok_type == 'eval':
			result.add(PythonNode(parameters))

		# If an executed expression, add an ExecNode:
		elif tok_type == 'exec':
			result.add(ExecNode(parameters))

		# If an else, check for a matching if and recurse:
		elif tok_type == 'else':
			if last == 'if':
				return (result, parse_template(iterator, 'else')[0])
			else:
				raise NoMatchingEndToken('An "{% else %}" block was supplied without an "{% if %}" block.')

		# If an endif, check for a matching if/else and return:
		elif tok_type == 'endif':
			if last in ('if', 'else'):
				return (result, TextNode(''))
			else:
				raise NoMatchingEndToken('An "{% endif %}" block was supplied without an "{% if %}" block.')

		# If an endfor, check for a matching for and return:
		elif tok_type == 'endfor':
			if last == 'for':
				return result
			else:
				raise NoMatchingEndToken('An "{% endfor %}" block was supplied without a "{% for %}" block.')

		# If an if, recurse for the containing blocks, and add an IfNode:
		elif tok_type == 'if':
			istrue, isfalse = parse_template(iterator, 'if')
			result.add(IfNode(parameters, istrue, isfalse))

		# If a for, recurse for the contained blocks and add a ForNode:
		elif tok_type == 'for':
			variables, iterable = parameters
			result.add(ForNode(variables, iterable, parse_template(iterator, 'for')))

		# Inline if - create an IfNode with python nodes as children:
		elif tok_type == 'iif':
			condition, istrue = parameters
			result.add(IfNode(condition, PythonNode(istrue), TextNode('')))

		# Inline if with else:
		elif tok_type == 'iif_else':
			condition, istrue, isfalse = parameters
			result.add(IfNode(condition, PythonNode(istrue), PythonNode(isfalse)))

		# If an include, recursively parse the file:
		elif tok_type == 'include':
			result.add(parse_file(parameters))

		# If a remapping include, construct a node for remapping the variables:
		elif tok_type == 'include_remap':
			filename, variables = parameters
			result.add(IncludeNode(parse_file(filename), variables.split(';')))

		# If a comment, ignore:
		elif tok_type == 'comment':
			pass # Ignore


		### Special tokens! ###
		
		# Gravatar URLs:
		elif tok_type == 'gravatar':
			result.add(GravatarNode(parameters))


	# If a block was not terminated, raise an exception:
	if last is not None:
		raise NoMatchingEndToken('The end the input was reached before an {} block was closed.'.format('{% '+last+' %}'))

	# Return the GroupNode:
	return result


def render(template, variables={}):
	"""
	Renders a template string as text
	Returns rendered template

	>>> render("{{string}}", variables={'string': 'this is a string'})
	'this is a string'
	"""
	return parse(template).render(dict(variables.items()))


def render_file(filename, variables={}):
	"""
	Call with the relative path of the template as filename, and the list of variables as variables
	"""
	return parse_file(filename).render(dict(variables.items()))


if __name__ == '__main__':
	context = {
		'user': 'Bob',
		'friends': ['James', 'Dom', 'Who', 'The Doctor'],
		'age': 17
	}
	
	result = """Bob's Page:
 				0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49 
				I have 4:
				<ul>	<li>		James			(poor effort of a name)			</li>	<li>		Dom			(poor effort of a name)		
				</li>	<li>		Who			(poor effort of a name)	</li>	<li>		The Doctor 		(that's a really long name!)
				</li></ul><img src="http://www.gravatar.com/avatar/5730cd5627b5cbed1c4b7b5f89fa9bd2"/>"""
	
	template = """{{ user }}'s Page:{% for i in range(50) %} {{i}} {% endfor %}I have {{ len(friends) }}:<ul>	{% for friend in friends %}	<li>
				{{friend}}		{% if len(friend) > (1000//160) %}			(that's a really long name!)		{% else %}			(poor effort of a name)
				{% endif %}	</li>	{% endfor %}</ul><img src="{% gravatar 'jack.thatch@gmail.com' %}"/>{# this is a comment! #}{# I could {% include "footer.html" %} if I wanted to! #}""".replace('\n','')

	assert render(template, context).replace('\n','').replace(' ','').replace('\t','') == result.replace('\n','').replace(' ','').replace('\t','')