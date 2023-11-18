from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import random
import json
import requests

app = Flask(__name__)

# Leer fraudTest.csv
df_directory = os.path.join(os.path.dirname(__file__), 'dataset', 'fraudTest.csv')
df = pd.read_csv(df_directory)

# Cargar la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Obtener una linea del dataset
@app.route('/getTransRow')
def getTransRow():
    index = random.randint(0, len(df) - 1)
    row = df.iloc[index]
    specific_data = {
        'Name': row['first'],
        'Last': row['last'],
        'TransCategoy': row['category']
    }
    
    # Saving row as a json
    json_row_dir = os.path.join(os.path.dirname(__file__), '../wspace2/json')
    if not os.path.exists(json_row_dir):
        os.makedirs(json_row_dir)
        
    json_file = os.path.join(json_row_dir, 'row.json')
    with open(json_file, 'w') as json_file:
        json.dump(index, json_file)
    
    #print(specific_data)
    return json.dumps(specific_data)

if __name__ == '__main__':
    app.run()
