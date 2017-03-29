import codecs
import sys
import unittest

from sklearn.feature_extraction import dict_vectorizer
import numpy as np
from sklearn.model_selection import train_test_split
from os import walk

# train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
# test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation

train_path = "test_data/aclImdb/train/"  # use terminal to ls files under this directory
test_path = "test_data/imdb_te.csv"  # test data for grade evaluation
stopwords_path = "test_data/stopwords.en.txt"
stop_words = None


def get_all_files(mypath):
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    return f


def read_stopwords():
    with open(stopwords_path, 'r') as fi:
        data = fi.readlines()
        return data


def process_file_contents(s):
    global stop_words
    import re

    if stop_words is None:
        stop_words = read_stopwords()
        stop_words = set([s.strip() for s in stop_words])

    # words = re.findall(r"[\w']+", s)
    words = s.replace('"', '""').split()
    result = [word for word in words if word not in stop_words]
    return " ".join(result)


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    """Implement this module to extract
   and combine text files under train_path directory into
   imdb_tr.csv. Each text file in train_path should be stored
   as a row in imdb_tr.csv. And imdb_tr.csv should have two
   columns, "text" and label"""

    # first get all of the positive reviews
    row_counter = 0
    with open(outpath + name, 'w') as fo:
        fo.write("%s, %s, %s\n" % ("row_counter", "text", "polarity"))
        root_path = inpath  + train_path + "pos/"
        review_files = get_all_files(root_path)
        for filename in review_files:
            output_processed_row(fo, root_path+filename, row_counter, 1)
            row_counter += 1

        root_path = inpath + train_path + "neg/"
        review_files = get_all_files(root_path)
        for filename in review_files:
            output_processed_row(fo, root_path+filename, row_counter, 0)
            row_counter += 1


def output_processed_row(fo, path, row, polarity):
    # with codecs.open(path, "r", encoding='utf-8', errors='ignore') as fi:
    with open(path, 'r', encoding="ascii", errors='ignore') as fi:
        try:
            text = fi.read()
        except Exception as inst:
            print("error handling", path)
            print(type(inst))
            print(inst.args)
            print(inst)
        else:
            text = process_file_contents(text)
            fo.write("%d, \"%s\", %d\n" % (row, text, polarity))


def main():
    training_data, test_data, training_labels, test_labels = import_and_scale_training_data(sys.argv[1])
    ngrams = create_ngrams(training_data, kind='unigram')
    model = train_model(ngrams, training_data, training_labels)
    results = test_model(model, test_data, test_labels)
    output_results(results)


if __name__ == "__main__":
    '''train a SGD classifier using unigram representation,
   predict sentiments on imdb_te.csv, and write output to
   unigram.output.txt'''

    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''

    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write
    output to unigram.output.txt'''

    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write
    output to unigram.output.txt'''
    main()


def get_data(input_filename, delimiter=','):
    with open(input_filename, 'r+b') as f:
        for record in f:  # traverse sequentially through the file
            x = record.split(delimiter)  # parsing logic goes here (binary, text, JSON, markup, etc)
            yield x  # emit a stream of things
            #  (e.g., words in the line of a text file,
            #   or fields in the row of a CSV file)


def import_and_scale_training_data(input_file_path):
    raw_data = np.loadtxt(input_file_path, delimiter=',', skiprows=1)
    x_train, x_test, y_train, y_test = train_test_split(raw_data[:, [0, 1]], raw_data[:, [2]].flatten(), test_size=0.4,
                                                        random_state=42)
    return x_train, x_test, y_train, y_test


def create_ngrams(training_data, kind='bigram'):
    pass


def train_model(ngrams, training_data, training_labels):
    pass


def test_model(model, test_data, test_labels):
    pass


def output_results(results):
    pass

class XformerTests(unittest.TestCase):
    def test_run (self):
        imdb_data_preprocess('./')

