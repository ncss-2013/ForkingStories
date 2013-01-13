import Spellcheck.spellcheck as spell
import json
import string

def spellcheck(response):
    text = response.get_field('text', default='')
    if text:
        fixed = {}
        words = set(text.split())
        for word in words:
            if word[0] in string.ascii_uppercase:
                word = word.lower()
                word = word.strip(string.punctuation)
                result = spell.suggest_corrections(word)
                if result is not None:
                    result_2 = list()
                    for word_2 in result:
                        word_2 = word_2[0].upper() + word_2[1:]
                        result_2.append(word_2)
                    word = word[0].upper() + word[1:]
                    fixed[word] = result_2
            else:
                word = word.lower()
                word = word.strip(string.punctuation)
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
