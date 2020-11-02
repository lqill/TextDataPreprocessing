import pandas as pd
import textdistance as td
import re
import string
from nltk.corpus import words


class preprocessing():
    def stem(self, data):
        """
        cut words into efficiet to understand by computer
        """
        pass

    def lemmi(self, data):
        """
        convert words into a single base word
        """
        pass

    def funcname(self, parameter_list):
        """
        docstring
        """
        pass


class filtering():
    # word_filters can be adjuster to a set of choosen language
    word_filters = set(words.words())
    custom = []
    custom_filters = set([])

    def add_custom_words(self, list_of_words):
        # for adding custom words to filter
        custom.extend(list_of_words)
        custom_filters = set(custom)

    def reset_custom_words(self):
        custom_filters = set([])

    def more_english(self, text):
        # ignore this function, this is needed for func english only filter
        words_in_text = text.split(" ")
        eng_level = 0  # made up english level
        for word in words_in_text:
            if word in word_filters:
                eng_level += 1
            else:
                eng_level -= 1
        if eng_level >= 0:
            return True
        else:
            return False

    def english_only(self, data, col_name):
        '''
        data => dataframe that will be filtered
        col_name => the column name which the filter will be based on
        The dataFrame will be filtered by nltk words collection.Meaning, it is based on nltk words.words
        '''
        data["english"] = data[col_name].apply(more_english)
        data = data[data["english"]]
        data = data.drop(["english"], axis=1)
        return data

    def filter_on(self, text):
        words_in_text = text.split(" ")
        for word in words_in_text:
            if word in custom_filters:
                return True
            else:
                return False

    def filter(self, data, col_name):
        data["filter"] = data[col_name].apply(filter_on)
        data = data[data["filter"]]
        data = data.drop(["filter"], axis=1)
        return data


class cleaning():
    def number(self, text):
        # remove number
        return re.sub(r'\d+', '', text.lower())

    def punctuation(self, text):
        # remove punctuation
        return text.translate(str.maketrans("", "", string.punctuation))

    def whitespace(self, text):
        # remove whitespace
        return text.strip()

    def all(self, text):
        # all of the above and lower too
        text = text.lower()
        text = number(text)
        text = punctuation(text)
        text = whitespace(text)
        return text


class modeling():
    pass
