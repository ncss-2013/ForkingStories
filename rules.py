import re

class Rules(object):
#    def __init__(self, condition):
#        self.condition = condition

    def letters_per_word(original:str, minimum:int=0, maximum:int=999):
        '''
Returns False if the word is not within (or equal to) the minimum or maximum
values set by the user.
        '''
        text = original.lower()
        eng_words = re.findall(r"[a-z'/-]+", text)        
        for word in eng_words:
            if not minimum <= len(word) <= maximum:
                return False
        return True


    def ban_on_words(original:str, banned_words:list,):
        '''
Returns False if a banned word is found within the text.
        '''
        for word in banned_words:
             if re.search(r"\b{}\b".format(word), original, flags=re.IGNORECASE):
                 return False
        return True
    


    def max_num_words(text, limit):
        # the number of words in submission must be <= host input
        """ This is my documentation.

         max_num_words("hello", 5)
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
    #import doctest
    #doctest.testmod()
    #these are tests for this function
    assert Rules.max_num_words("hello", 5)
    assert not Rules.max_num_words("hello hello hello", 2)
    assert Rules.max_num_words("hello hello", 2)
    assert Rules.max_num_words("", 3)
    assert not Rules.max_num_words("hello blah", -3)

    assert not Rules.include_words("banana", "c")
    assert Rules.include_words("hello banana apple", "apple")
    assert not Rules.include_words("hello banana apple", "ban")
    assert Rules.include_words("hello banana apple", "")
    assert Rules.include_words("hello banana apple", "hello banana")
    assert not Rules.include_words("hello banana apple", "hello train")
    assert Rules.include_words("hello banana apple", ["hello", "apple"])
    

    
    # Waseem - letters_per_word and ban_on_words
    
    assert not Rules.letters_per_word("cat it's", maximum = 3)
    assert Rules.letters_per_word("c-d", minimum = 3)
    assert Rules.letters_per_word("", minimum = 2)

    assert Rules.ban_on_words("cation, organic", ['cat', 'gan'])
    assert not Rules.ban_on_words("cat's, organic", ['cat', 'gan'])
    assert Rules.ban_on_words("fjkalsd", [])
    assert not Rules.ban_on_words("blah blah blah", ['abc', 'blah'])

                     
                             
    
    
