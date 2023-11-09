from flask import Flask, render_template, Response, send_from_directory
from sklearn.preprocessing import StandardScaler
import json
import os
import time
import pandas as pd
import tensorflow as tf
import numpy as np

app = Flask(__name__)

json_folder = os.path.join(os.path.dirname(__file__), 'json')
print(json_folder)
model_folder = os.path.join(os.path.dirname(__file__), 'modelo', 'detectorV2.h5')
print(model_folder)
model = tf.keras.models.load_model(model_folder)

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
    csv_file = os.path.join(os.path.dirname(__file__), 'fraudTest.csv')
    dataRaw = pd.read_csv(csv_file)
    # en caso de fallo utilizar https://drive.google.com/file/d/1tV4hk-HvnWZPo5WvAl82-STOuTvKkVAN/view?usp=sharing
    # dataRaw = pd.read_csv('fraudTrain.csv')
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
        if data:
            if data != last_json:
                last_json = data
                json_data = pd.DataFrame([data])
                json_data = preProcess_data(json_data)
                predict = model.predict(json_data)
                predicted = (predict > 0.5).astype(float)
                print(predicted)
                if predicted[0][0] == 1.0:
                    yield f"data: {json.dumps(data)}\n\n"
        time.sleep(2)  # Comprueba cada 2 segundos si hay cambios en la carpeta JSON

@app.route('/')
def mostrar_json():
    data = get_latest_json()
    return render_template('monitor.html', data=data)

@app.route('/events')
def sse():
    return Response(generate_events(), content_type='text/event-stream')

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(port=5001, threaded=True)