import pandas as pd
import numpy as np

def cleaning():
    df = pd.read_csv('/home/mostafa/Desktop/FSD Projects/big_mart/dags/data/data.csv')

    df['Item_Weight'] = df['Item_Weight'].fillna(df['Item_Weight'].mean())

    df['Item_Fat_Content'] = df['Item_Fat_Content'].map({'LF':'Low Fat', 'Low Fat':'Low Fat',
                                                        'low fat':'Low Fat', 
                                                        'reg':'Regular', 'Regular':'Regular'})
                                            
    df['Outlet_Size'] = df['Outlet_Size'].apply(lambda x: np.random.choice(df['Outlet_Size'].dropna().unique()) if pd.isnull(x) else x)

    grouped_means = df.groupby(['Outlet_Location_Type', 'Outlet_Type'])['Item_Outlet_Sales'].transform('mean')
    df['Item_Outlet_Sales'] = df['Item_Outlet_Sales'].fillna(grouped_means)

    df.drop(columns=['source'], axis=1, inplace=True)

    columns_dict = {}

    for column in df.iloc[:, 1:].select_dtypes(include=['object']).columns:
        columns_dict[column] = pd.DataFrame(df[column].unique()).iloc[:, 0].to_dict()

    columns_dict_rev = {key: {v: k for k, v in value.items()} for key, value in columns_dict.items()}

    dvc_df = df.copy()

    for column in columns_dict_rev.keys():
        dvc_df[column] = dvc_df[column].map(columns_dict_rev[column])

    dvc_df.to_csv('/home/mostafa/Desktop/FSD Projects/big_mart/dags/data/dvc_df.csv')
    df.to_csv('/home/mostafa/Desktop/FSD Projects/big_mart/dags/data/df.csv')

    print(df.head())