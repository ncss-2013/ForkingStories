# This is a short example of how to use the templating engine.
# It uses the template "template_example.html"

# First we import the module:
import template

# These are the variables the template can use:
context = {
	'user': 'Bob',
	'friends': ['James', 'Dom', 'Who', 'The Doctor'],
	'age': 17
}

# We call render_file to render the template to a string:
html = template.render_file('templates/template_example.html', context)

print(html)