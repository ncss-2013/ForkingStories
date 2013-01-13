import Spellcheck.spellcheck as spell
import json

def spellcheck(response):
    text = response.get_field('text', default='')
    if text:
        fixed = {}
        words = set(text.split())
        for word in words:
            result = spell.suggest_corrections(word)
            if result is not None:
                fixed[word] = result
        response.write(json.dumps(fixed))

    else:
        response.write("Hello! This is probably a spellchecker of some kind.")
        response.write('''
<form method='post'>
<textarea name='text'>
</textarea>
<input type='submit' />
</form>
''')
