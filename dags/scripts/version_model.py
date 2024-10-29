import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
from datetime import datetime
# from train_model import train_model
# import warnings
# warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import dvc.api, dvc.repo
import io
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

def train_model():
    url = "https://github.com/mostafa-fallaha/big-mart.git"
    data = dvc.api.read("dags/data/dvc_df.csv", repo=url)
    df = pd.read_csv(io.StringIO(data))

    df.drop(columns=['Unnamed: 0', 'Item_Identifier'], axis=1, inplace=True)

    # Features Selection
    X_tmp = df.drop('Item_Outlet_Sales', axis=1)
    y_tmp = df['Item_Outlet_Sales']

    model = RandomForestRegressor(random_state=42)
    model.fit(X_tmp, y_tmp)

    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': X_tmp.columns, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    features = feature_importance_df.loc[feature_importance_df['Importance'] >= 0.05, 'Feature'].to_list()

    X = df[features]
    y = df['Item_Outlet_Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    poly = PolynomialFeatures(5, interaction_only=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    linear_poly = LinearRegression()
    linear_poly.fit(X_train_poly, y_train)
    # y_pred_poly = linear_poly.predict(X_test_poly)
    # print(root_mean_squared_error(y_test, y_pred_poly))
    return linear_poly, X_test, X_test_poly, y_test

def version_model():
    runname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    mlflow.set_experiment('big_mart_model')
    with mlflow.start_run(run_name=runname) as mlflow_run:
        run_id = mlflow_run.info.run_id

        linear_poly, X_test, X_test_poly, y_test = train_model()

        # =========== Model metrics ======================
        y_pred = linear_poly.predict(X_test_poly)

        rmse = root_mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        # =========== Model versioning ======================
        signature = infer_signature(X_test, y_test)

        mlflow.log_params({'Polynomial Degree': 5})

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(
            sk_model=linear_poly,
            artifact_path="linear_poly_model",
            signature=signature,
            registered_model_name="linear_poly_registered_model"
        )