import pickle
import numpy as np

def load_model():
    try:
        model = pickle.load(open("model/model.pkl", "rb"))
        return model
    except:
        return None

def run_prediction(model, features):
    if model is None:
        raise Exception("ML model not loaded.")
    features = np.array(features).reshape(1, -1)
    return float(model.predict(features)[0])
