import pandas as pd
import numpy as np
import json


class Preprocessor:
    def __init__(self):
        pass

    def preprocess(self, products):
        """ [product = {
            "id": "some_id_3",
            "name": "Название товара3",
            "props": [...]
          }, ...]"""
        return pd.DataFrame() #ready for model

    def preprocess_dataset(self, path):
        # output: data with columns, target column class with class numbers, array where [i] -> name of class number i
        return pd.DataFrame(), np.array()

    def generate_dataset(self, in_path, out_path):
        # path to json, path to csv (and also the classes ids -> classes in file with the same name)
        pass