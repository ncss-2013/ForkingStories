
def max_num_words(text, limit):
    # the number of words in submission must be <= host input
    """ This is my documentation.

    >>> max_num_words("hello", 5)
    True
    """
    words = text.split()
    if len(words) <= limit:
        return True
    else:
        return False

def include_words(text, forcedwords):
    #users text must include the words host submits
    if type(forcedwords) == str:
        forcedwords = forcedwords.split(" ")
    text = text.lower().split(" ")        
    for word in forcedwords:
        if word and word.lower() not in text:
            return False
    return True

def include_number_words(text, required_word, number):
    #host sets requirement for certain word to be used in writers submission every ___ words
    words = text.split()
    count = 0
    for word in words:
        if word == required_word:
            count = 0
        else:
            count += 1
        if count >= number:
            return False
    return True    
        
        


if __name__=="__main__":
    import doctest
    doctest.testmod()
    #these are tests for this function
    assert max_num_words("hello", 5)
    assert not max_num_words("hello hello hello", 2)
    assert max_num_words("hello hello", 2)
    assert max_num_words("", 3)
    assert not max_num_words("hello blah", -3)

    assert not include_words("banana", "c")
    assert include_words("hello banana apple", "apple")
    assert not include_words("hello banana apple", "ban")
    assert include_words("hello banana apple", "")
    assert include_words("hello banana apple", "hello banana")
    assert not include_words("hello banana apple", "hello train")
    assert include_words("hello banana apple", ["hello", "apple"])
    
                         
                             
    
    
