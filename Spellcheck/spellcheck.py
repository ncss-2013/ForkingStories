import string
import os

if __name__ == "__main__":
    basepath = "."
else:
    basepath = os.path.dirname(__file__)

file = open(basepath+'/words.txt')
dictionary = set()
for line in file:
    dictionary.add(line[:-1])

test = dict()
with open(basepath+'/wordcount.txt', encoding='utf-8') as w:
    for line in w:
        line = line.split()
        word = line[0]
        value = int(line[1])
        test[word] = value

def generate_deletions(word):
    new_words = set()
    for i in range(len(word)):
        new_word = word[:i] + word[i+1:]
        new_words.add(new_word)
    return new_words

def generate_insertions(word):
    new_words = set()
    for letter in string.ascii_lowercase:
        new_word = letter + word
        new_words.add(new_word)
        for i in range(len(word)):
            new_word = word[:i] + letter + word[i:]
            new_words.add(new_word)
        new_word = word + letter
        new_words.add(new_word)
    for letter in string.ascii_uppercase:
        new_word = letter + word
        new_words.add(new_word)
        for i in range(len(word)):
            new_word = word[:i] + letter + word[i:]
            new_words.add(new_word)
        new_word = word + letter
        new_words.add(new_word)
    return new_words

def generate_replacements(word):
    new_words = set()
    for letter in string.ascii_lowercase:
        new_word = letter + word[1:]
        new_words.add(new_word)
        for i in range(len(word)):
            new_word = word[:i] + letter + word[i+1:]
            new_words.add(new_word)
    for letter in string.ascii_uppercase:
        new_word = letter + word[1:]
        new_words.add(new_word)
        for i in range(len(word)):
            new_word = word[:i] + letter + word[i+1:]
            new_words.add(new_word)
    return new_words

def generate_transpositions(word):
    new_words = set()
    if len(word) < 2:
        new_words.add('')
        return new_words
    new_word = word[1] + word[0] + word[2:]
    new_words.add(new_word)
    for i in range(len(word)-1):
        new_word = word[:i] + word[i+1]+ word[i] + word[i+2:]
        new_words.add(new_word)
    new_word = word[:-2] + word[-1]+ word[-2]
    new_words.add(new_word)
    return new_words

def check_spelling(word):
    suggestions = set()
    suggestions_2 = dict()
    all_suggestions = set()
    if word in dictionary:
        suggestions_2[word] = 1
        return suggestions_2
    deletions = generate_deletions(word)
    insertions = generate_insertions(word)
    replacements = generate_replacements(word)
    transpositions = generate_transpositions(word)
    for new_word in deletions:
        if new_word in dictionary:
            suggestions.add(new_word)
        all_suggestions.add(new_word)
    for new_word in insertions:
        if new_word in dictionary:
            suggestions.add(new_word)
        all_suggestions.add(new_word)
    for new_word in replacements:
        if new_word in dictionary:
            suggestions.add(new_word)
        all_suggestions.add(new_word)
    for new_word in transpositions:
        if new_word in dictionary:
            suggestions.add(new_word)
        all_suggestions.add(new_word)
    for new_word in all_suggestions:
        deletions_2 = generate_deletions(new_word)
        insertions_2 = generate_insertions(new_word)
        replacements_2 = generate_replacements(new_word)
        transpositions_2 = generate_transpositions(new_word)
        for new_word_2 in deletions_2:
            if new_word_2 in dictionary:
                if new_word_2 in suggestions_2:
                    suggestions_2[new_word_2] += 1
                else:
                    suggestions_2[new_word_2] = 1
        for new_word_2 in insertions_2:
            if new_word_2 in dictionary:
                if new_word_2 in suggestions_2:
                    suggestions_2[new_word_2] += 1
                else:
                    suggestions_2[new_word_2] = 1
        for new_word_2 in replacements_2:
            if new_word_2 in dictionary:
                if new_word_2 in suggestions_2:
                    suggestions_2[new_word_2] += 1
                else:
                    suggestions_2[new_word_2] = 1
        for new_word_2 in transpositions_2:
            if new_word_2 in dictionary:
                if new_word_2 in suggestions_2:
                    suggestions_2[new_word_2] += 1
                else:
                    suggestions_2[new_word_2] = 1
    for new_word in suggestions:
        if new_word in suggestions_2:
            suggestions_2[new_word] += 1
        else:
            suggestions_2[new_word] = 1
    return suggestions_2

def suggest_corrections(word):
    suggestions = check_spelling(word)
    suggestions_2 = dict()
    final = list()
    for i in suggestions:
        if i in test:
            suggestions_2[i] = suggestions[i] * test[i]
        else:
            suggestions_2[i] = suggestions[i]
    sorted_suggestions = sorted(suggestions_2.items(), key=lambda x: x[1], reverse=True)
    for items in sorted_suggestions:
        item_1, item_2 = items
        final.append(item_1)
    if word in final:
        return None
    elif len(final) >= 10:
        return final[:10]
    return final

if __name__ == '__main__':
    word = input('Enter word: ')
    while word:
        results = suggest_corrections(word)
        if word is None:
            print('No errors!')
        elif len(results) == 0:
            print('No results!')
        else:
            for index in range(10):
                print(results[index],)
        print()
        word = input('Enter word: ')
