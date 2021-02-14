import pandas as pd
# preprocessing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# filtering
from nltk.corpus import words as nltk_words

# cleaning
import re
import string

# modeling
from sklearn.preprocessing import LabelEncoder

# TODO: print function output like data length before/after or may removed or anything like function done or other output
# TODO: modelling need more or gonna be moved to a seperate file with text conversion or crossdata


class preprocessing:
    # This function contain lemmatiation, Stemmer, and StopWords removal
    def __init__(self, mode="eng"):
        print(mode)
        self.mode = mode
        if self.mode == "ind":
            self.stop_words = set(stopwords.words('indonesian'))
            factory = StemmerFactory()
            self.stemmer = factory.create_stemmer()
        else:
            self.lemmatizer = WordNetLemmatizer()
            self.stemmer = PorterStemmer()
            self.stop_words = set(stopwords.words())

    def token(self, text):
        return word_tokenize(text)

    def stem(self, text):
        return [self.stemmer.stem(w) for w in text]

    def lemmi(self, text):
        if self.mode != "ind":
            return [self.lemmatizer.lemmatize(w) for w in text]
        else:
            return text

    def stopword(self, text):
        text=[w for w in text if w not " "]
        return [w for w in text if w not in self.stop_words]

    def all(self, dataframe, column_name):
        dataframe[column_name] = dataframe[column_name].apply(
            lambda text: self.stem(self.lemmi(self.stopword(self.token(text)))))
        return dataframe


class filtering:
    # word_filters can be adjuster to a set of choosen language
    def __init__(self):
        self.word_filters = set(nltk_words.words())
        self.custom = []
        self.custom_filters = set([])

    def add_custom_words(self, list_of_words):
        # for adding custom words to filter
        self.custom.extend(list_of_words)
        self.custom_filters = set(self.custom)

    def reset_custom_words(self):
        self.custom_filters = set([])

    def more_english(self, text):
        # ignore this function, this is needed for func english only filter
        words_in_text = text.split(" ")
        eng_level = 0  # made up english level
        for word in words_in_text:
            if word in self.word_filters:
                eng_level += 1
            else:
                eng_level -= 1
        if eng_level >= 0:
            return True
        else:
            return False

    def english_only(self, dataframe, column_name):
        # The dataFrame will be filtered by nltk words collection.Meaning, it is based on nltk words.words
        before = len(dataframe)
        dataframe["english"] = dataframe[column_name].apply(self.more_english)
        dataframe = dataframe[dataframe["english"]]
        dataframe = dataframe.drop(["english"], axis=1)
        dataframe = dataframe.reset_index(Drop=True)
        after = len(dataframe)
        print("FILTER done. {} -> {} , {}removed".format(before, after, before-after))
        return dataframe

    def filter_on(self, text):
        words_in_text = text.split(" ")
        for word in words_in_text:
            if word not in self.custom_filters:
                return True
            else:
                return False

    def filter(self, dataframe, col_name):
        # filtering dataframe so the resulting dataframe contain no dataframe
        before = len(dataframe)
        dataframe["filter"] = dataframe[col_name].apply(self.filter_on)
        dataframe = dataframe[dataframe["filter"]]
        dataframe = dataframe.drop(["filter"], axis=1)
        dataframe = dataframe.reset_index(Drop=True)
        after = len(dataframe)
        print("FILTER done. {} -> {} , {}removed".format(before, after, before-after))
        return dataframe


class cleaning:
    def number(self, text):
        # remove number
        return re.sub(r'\d+', '', text.lower())

    def punctuation(self, text):
        # remove punctuation
        return text.translate(str.maketrans("", "", string.punctuation))

    def whitespace(self, text):
        # remove whitespace
        return text.strip()

    def clean(self, text):
        # all of the above and lower too
        text = text.lower()
        text = self.number(text)
        text = self.punctuation(text)
        text = self.whitespace(text)
        return text


class modeling:
    def __init__(self):
        self.le = LabelEncoder()

    def label_encode(self, dataframe, column_name):
        dataframe[column_name] = self.le.fit_transform(dataframe[column_name])
        print(dataframe[column_name].value_counts())
        return dataframe


# debugging

def main():
    text = "i am going to buy some unused car and writing this letter seems like a waste of time for me"
    print("start debugging")
    print("breakpoint")
    print("done debugging")


if __name__ == "__main__":
    main()
