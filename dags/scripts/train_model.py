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
    y_pred_poly = linear_poly.predict(X_test_poly)
    print(root_mean_squared_error(y_test, y_pred_poly))