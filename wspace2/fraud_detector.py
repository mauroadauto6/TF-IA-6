from flask import Flask, render_template, Response
from sklearn.preprocessing import StandardScaler
import json
import os
import time
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

json_folder = os.path.join(os.path.dirname(__file__), 'json')
print(json_folder)
model_folder = os.path.join(os.path.dirname(__file__), 'modelo', 'detectorV6.h5') # FINAL VERSION
print(model_folder)
model = tf.keras.models.load_model(model_folder)
# Read the dataset
df_directory = os.path.join(os.path.dirname(__file__), 'dataset', 'fraudTest.csv')
dataRaw = pd.read_csv(df_directory)
# Clean dataset
# prediction dataset
columns_out = ['Unnamed: 0', 'cc_num', 'merchant', 'state', 'first', 'last', 'gender', 'street', 'city', 'zip', 'city', 'job', 'dob', 'trans_num', 'unix_time']
testData = dataRaw.drop(columns=columns_out)
# to be shown dataset
another_col_out = ['Unnamed: 0', 'merchant', 'gender', 'street', 'job', 'dob', 'trans_num', 'unix_time']
showData = dataRaw.drop(columns=another_col_out)
# Dataset Headers
headers = testData.columns.tolist()
complete_headers = showData.columns.tolist()
# General dataframe for prediction
purchaseData = pd.DataFrame(index=[0], columns=headers)
printData = pd.DataFrame(index=[0], columns=complete_headers)
# Dataset Category Headers
categories = testData['category'].unique()
OH_categories = pd.DataFrame(False, index=[0], columns=[f'cat_{category}' for category in categories])


def get_index_json():
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    if json_files:
        latest_json = max(json_files, key=lambda x: os.path.getctime(os.path.join(json_folder, x)))
        with open(os.path.join(json_folder, latest_json), 'r') as archivo_json:
            return json.load(archivo_json)
    return None

def preProcess_data(purchaseData):
    # One-hot encoding for categories
    X = pd.get_dummies(purchaseData, columns=['category'], prefix=['cat'])
    X = X.drop(columns=['is_fraud'])
    
    # Obtain the common column between 'X' and 'One-Hot categories'
    common_col = X.columns.intersection(OH_categories.columns).tolist()
    
    # Replacing the value of the same category 
    aux_OH_categories = OH_categories
    aux_OH_categories[common_col] = X[common_col]
    
    # Drop the common column in 'X'
    new_X = X.drop(columns=common_col)
    
    # Final row to predict
    final_row = pd.concat((new_X, aux_OH_categories), axis=1)
    
    # Date encoding
    final_row['hour'] = pd.to_datetime(testData['trans_date_trans_time']).dt.hour
    final_row['day'] = pd.to_datetime(testData['trans_date_trans_time']).dt.day_of_week
    final_row['month'] = pd.to_datetime(testData['trans_date_trans_time']).dt.month
    final_row = final_row.drop(columns=['trans_date_trans_time'])
    #print(final_row)
    
    # Scale
    scaler = StandardScaler()
    final_row = scaler.fit_transform(final_row)
    final_row = scaler.transform(final_row)
    
    return final_row

def generate_events():
    print('EVENT')
    while True:
        # Obtain one random row from the dataset to be preditec
        data_index = get_index_json()
        row_data = testData.iloc[data_index].tolist()
        purchaseData.loc[0] = row_data
        
        # Prepare data to be shown
        sh_row_data = showData.iloc[data_index].tolist()
        printData.loc[0] = sh_row_data
        print(purchaseData.head())
        if not purchaseData.empty:
            data = preProcess_data(purchaseData)
            predict = model.predict(data)
            predicted = (predict > 0.5).astype(int)
            print('Tag:{}, Prediction:{}%'.format(purchaseData['is_fraud'], predicted[0][0]*100))
            if predicted[0][0] == 1:
                yield f"data: {json.dumps(printData.head().to_dict(orient='records'))}\n\n"
        time.sleep(3.5) 

@app.route('/')
def show_data():
    data_index = get_index_json()
    row_data = showData.iloc[data_index].tolist()
    printData.loc[0] = row_data
    data = printData.head().to_dict(orient='records')
    print(data)
    return render_template('fraud_detector.html', data=data)

@app.route('/events')
def sse():
    return Response(generate_events(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(port=5001, threaded=True)