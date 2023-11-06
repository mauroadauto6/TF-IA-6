from flask import Flask, render_template, Response, send_from_directory
from sklearn.preprocessing import StandardScaler
import json
import os
import time
import pandas as pd
import tensorflow as tf
import numpy as np

json_folder = os.path.join(os.path.dirname(__file__), 'json')
print(json_folder)
model = tf.keras.models.load_model('detectorV2.h5')

def get_latest_json():
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    if json_files:
        latest_json = max(json_files, key=lambda x: os.path.getctime(os.path.join(json_folder, x)))
        with open(os.path.join(json_folder, latest_json), 'r') as archivo_json:
            return json.load(archivo_json)
    return None

def preProcess_data(purchaseData):
    columns_out = ['Unnamed: 0', 'cc_num', 'merchant', 'state', 'first', 'last', 'gender', 'street', 'city', 'zip', 'city', 'job', 'dob', 'trans_num', 'unix_time']
    # Leer un csv con todas las variables
    dataRaw = pd.read_csv('fraudTest.csv')
    dataRaw = dataRaw.drop(columns=columns_out)
    purchaseData = purchaseData.drop(columns=columns_out)
    # Guardar solo categorias en otra variable
    categories = dataRaw['category'].unique()
    OH_categories = pd.DataFrame(False, index=[0], columns=[f'cat_{category}' for category in categories])
    
    X = pd.get_dummies(purchaseData, columns=['category'], prefix=['cat'])
    X = X.drop(columns=['is_fraud'])
    print(X)
    common_columns = OH_categories.columns.intersection(X.columns).tolist()
    OH_categories = OH_categories[OH_categories.columns.difference(common_columns)]
    
    X = pd.concat([X, OH_categories], axis=1)
    
    X['hour'] = pd.to_datetime(purchaseData['trans_date_trans_time']).dt.hour
    X['day'] = pd.to_datetime(purchaseData['trans_date_trans_time']).dt.dayofweek
    X['month'] = pd.to_datetime(purchaseData['trans_date_trans_time']).dt.month
    X = X.drop(columns=['trans_date_trans_time'])
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X = scaler.transform(X)
    print(X.shape)
    print(X)
    return X

def generate_events():
    last_json = None
    print('EVENT')
    while True:
        data = get_latest_json()
        if data and data.get('is_fraud') == 1:
            if data != last_json:
                last_json = data
                json_data = pd.DataFrame([data])
                json_data = preProcess_data(json_data)
                prediction = model.predict(json_data)
                if prediction[0][0] == 1.0:
                    print(data)
        time.sleep(2)  #

generate_events()