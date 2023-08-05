import os
import joblib
import numpy as np
import pandas as pd
from scipy.stats import skew
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

SELECTED_FEATURES = [
    'powerPS', 'vehicleType', 'brand',
    'fuelType', 'kilometer', 'price'
]
SELECTED_PREDICTORS = [
    'powerPS', 'vehicleType', 'brand',
    'fuelType', 'kilometer'
]
CONTINUOUS_FEATURES = ['powerPS', 'kilometer', 'price']
CONTINUOUS_PREDICTORS = ['powerPS', 'kilometer']
CATEGORICAL_FEATURES = ['vehicleType', 'brand', 'fuelType']
TARGET_FEATURE = 'price'

IMPUTER_FILENAME = 'imputer.joblib'
PIPELINE_FILENAME = 'pipeline.joblib'
SKEWED_PREDICTORS = 'skewed_predictors.joblib'


def save_object(obj, filename):
    current_working_dir = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_working_dir, 'models', filename)
    joblib.dump(obj, file_path)


def load_object(filename):
    current_working_dir = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_working_dir, 'models', filename)
    obj = joblib.load(file_path)
    return obj


def fix_data_type(data):
    fixed_data = data.astype({
        'powerPS': object
    })
    return fixed_data


def update_data_features(data_raw, features):
    return data_raw[features]


def clean_data(data_raw):
    updated_data_raw = update_data_features(
        data_raw, SELECTED_FEATURES
    )
    fixed_type_data_raw = fix_data_type(updated_data_raw)
    return fixed_type_data_raw


def clean_inference_data(data):
    updated_data_raw = update_data_features(
        data, SELECTED_PREDICTORS
    )
    fixed_type_data_raw = fix_data_type(updated_data_raw)
    return fixed_type_data_raw


def fix_data(data):
    data.drop_duplicates(inplace=True)
    data.drop(data[data['powerPS'] == 0].index, inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data


def handing_missing_values(data):
    si = SimpleImputer(strategy='constant', fill_value='any')
    si.fit(data[SELECTED_PREDICTORS])
    save_object(si, IMPUTER_FILENAME)


def fix_missing_values(data):
    si = load_object(IMPUTER_FILENAME)
    data.loc[:, SELECTED_PREDICTORS] = si.transform(
        data[SELECTED_PREDICTORS]
    )
    return data


def find_skewed_predictors(data):
    skewness = data[CONTINUOUS_PREDICTORS].apply(lambda x: skew(x))
    skewness = skewness[abs(skewness) > 0.5]
    skewed_features = skewness.index
    save_object(skewed_features, SKEWED_PREDICTORS)


def fix_predictor_skewness(data):
    skewed_features = load_object(SKEWED_PREDICTORS)
    data[skewed_features] = np.log1p(data[skewed_features].astype(float))
    return data


def fix_target_skewness(data):
    data[TARGET_FEATURE] = np.log1p(data[TARGET_FEATURE].astype(float))
    return data


def preprocess_for_build(data):
    fixed_data = fix_data(data)
    handing_missing_values(fixed_data)
    no_missing_array = fix_missing_values(fixed_data)
    no_missing_data = pd.DataFrame(no_missing_array, columns=SELECTED_FEATURES)
    find_skewed_predictors(no_missing_data)
    unskewed_predictors_data = fix_predictor_skewness(no_missing_data)
    unskewed_data = fix_target_skewness(unskewed_predictors_data)
    return unskewed_data


def preprocess_for_prediction(data):
    no_missing_data = fix_missing_values(data)
    unskewed_data = fix_predictor_skewness(no_missing_data)
    return unskewed_data


def split_train_data_raw(data, target_feature):
    X = data.drop(target_feature, axis=1)
    y = data[target_feature]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, random_state=0
    )

    return X_train, X_val, y_train, y_val


def build_pipeline():
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")
    numeric_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
            ("num", numeric_transformer, CONTINUOUS_PREDICTORS),
        ]
    )

    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestRegressor(
            n_estimators=50, max_depth=10, max_features="sqrt"
        ))
    ])
    return pipe


def train_model(X, y):
    # Train
    pipeline = build_pipeline()
    pipeline.fit(X, y)
    save_object(pipeline, PIPELINE_FILENAME)


def predict(data):
    pipeline = load_object(PIPELINE_FILENAME)
    y_pred = pipeline.predict(data)
    return y_pred
