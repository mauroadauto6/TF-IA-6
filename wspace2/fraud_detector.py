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
# Categories
categories = ['personal_care', 'health_fitness', 'misc_pos', 'travel', 'kids_pets', 'shopping_pos', 'food_dining', 'home', 'entertainment', 'shopping_net', 'misc_net', 'grocery_pos', 'gas_transport', 'grocery_net']
# Column out
columns_out = ['Unnamed: 0', 'cc_num', 'merchant', 'state', 'first', 'last', 'gender', 'street', 'city', 'zip', 'city', 'job', 'dob', 'trans_num', 'unix_time', 'is_fraud']

another_col_out = ['Unnamed: 0', 'merchant', 'gender', 'street', 'job', 'dob', 'trans_num', 'unix_time']
showData = dataRaw.drop(columns=another_col_out)
complete_headers = showData.columns.tolist()
printData = pd.DataFrame(index=[0], columns=complete_headers)

def get_index_json():
    json_file = os.path.join(json_folder, 'row.json')
    with open(json_file, 'r') as json_file:
        row = pd.read_json(json_file, orient='records')
    return row['Unnamed: 0'][0]

def preProcess_data(row_data):
    row_data = row_data.drop(columns=columns_out)
    
    # Category encoding
    categories = ['personal_care', 'health_fitness', 'misc_pos', 'travel', 'kids_pets', 'shopping_pos', 'food_dining', 'home', 'entertainment', 'shopping_net', 'misc_net', 'grocery_pos', 'gas_transport', 'grocery_net']
    for category in categories:
        row_data[f'cat_{category}'] = False
        
    index = row_data.index[0]   
    categ = row_data['category'][index]
    cat = 'cat_' + str(categ)
    
    # Replacing the same cat with True value
    if cat not in row_data.columns:
        row_data[cat] = False
    row_data.at[index, cat] = True
    
    # Date encoding
    row_data['hour'] = pd.to_datetime(row_data['trans_date_trans_time']).dt.hour
    row_data['day'] = pd.to_datetime(row_data['trans_date_trans_time']).dt.day_of_week
    row_data['month'] = pd.to_datetime(row_data['trans_date_trans_time']).dt.month
    row_data = row_data.drop(columns=['trans_date_trans_time'])
    row_data = row_data.drop(columns=['category'])
    
    # Scale
    scaler = StandardScaler()
    scaled_row= scaler.fit_transform(row_data)
    
    return scaled_row

def generate_events():
    print('EVENT')
    while True:
        json_file = os.path.join(json_folder, 'row.json')
        with open(json_file, 'r') as json_file:
            row = pd.read_json(json_file, orient='records')
        
        # Prepare data to be shown
        data_index = get_index_json()
        sh_row_data = showData.iloc[data_index].tolist()
        printData.loc[0] = sh_row_data
        
        if not row.empty:
            data = preProcess_data(row)
            predict = model.predict(data)
            predicted = (predict > 0.5).astype(int)
            print('Tag:{}, Prediction:{}%'.format(row['is_fraud'], predicted[0][0]*100))
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