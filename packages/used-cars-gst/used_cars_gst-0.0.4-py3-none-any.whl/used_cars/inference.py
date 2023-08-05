import pandas as pd
import numpy as np
from used_cars.preprocess import (
    clean_inference_data, preprocess_for_prediction,
    predict
)


def make_predictions(input_data_raw: pd.DataFrame):
    # the model and all the data preparation objects (encoder, etc) 
    # should be loaded from the models folder
    data = clean_inference_data(input_data_raw)
    preprocessed_data = preprocess_for_prediction(data)
    y_pred = predict(preprocessed_data)
    return np.expm1(y_pred)
