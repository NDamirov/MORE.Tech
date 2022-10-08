import numpy as np
import pandas as pd
import os

class DataLoader:
    def __init__(self, csv_path, class_ids_path):
        self.csv_path = os.path.normpath(csv_path)
        self.class_ids_path = os.path.normpath(class_ids_path)
        self.number_classes = 0
        self.number_features = 0

    def load(self):
        self.data = pd.read_csv(self.csv_path)
        self.classes = pd.read_csv(self.class_ids_path, index = "id")
        self.number_classes = self.classes.shape[0]
        self.number_features = self.data.shape[1] - 1

    def id_to_class(self, class_id):
        return self.classes.loc[class_id, "reference_id"]

def make_prediction(preprocessor, model, loader, products):
    preprocessed_data = preprocessor.preprocess(products)
    model_predictions = model.predict(preprocessed_data)  # class ids & None if not found
    np.apply_along_axis(loader.id_to_class, model_predictions[model_predictions != None])
    return model_predictions

if __name__ == "__main__":
    data = pd.read_csv("..//data//products//cleaned_data.csv")
    data.drop(columns = ["Unnamed: 0"], inplace=True)
    print(data.columns)
    print(data.iloc[0])