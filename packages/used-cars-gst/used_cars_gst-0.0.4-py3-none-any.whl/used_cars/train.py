import pandas as pd
from sklearn.metrics import mean_absolute_error
from used_cars.preprocess import (
    clean_data, preprocess_for_build,
    split_train_data_raw, train_model,
    predict
)
from used_cars.preprocess import (
    TARGET_FEATURE
)


def build_model(data_raw: pd.DataFrame):
    cleaned_data = clean_data(data_raw)
    preprocessed_data = preprocess_for_build(cleaned_data)
    X_train, X_val, y_train, y_val = split_train_data_raw(
        preprocessed_data, TARGET_FEATURE
    )
    # Train model and predict
    train_model(X_train, y_train)
    y_pred = predict(X_val)
    result = mean_absolute_error(y_val, y_pred)
    return result
