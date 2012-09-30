import numpy as np
import pymongo


def parse_file(filename, func=None):
    """
    Parses a file into data and returns a numpy array
    If a function is passed as func, then the function will be called on the
    the raw line of data to manipulate it as you want
    """
    data_file = open(filename, 'r')
    data_set = []
    for line in data_file.readlines():
        data_point = None
        if func:
            data_point = func(line)
        data_set.append(data_point)
    data_file.close()
    return np.array(data_set)


def train_troll_classifier():
    pass


def classify_comment_content_for_troll(content):
    pass