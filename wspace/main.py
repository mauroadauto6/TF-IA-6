from flask import Flask, render_template
import pandas as pd
import os
import json

app = Flask(__name__)

# Read the dataset
df_directory = os.path.join(os.path.dirname(__file__), 'dataset', 'fraudTest.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getTransRow')
def getTransRow():
    df = pd.read_csv(df_directory).sample(1)
    index = int(df.index[0])
    print(index)
    specific_data = {
        'Name': df['first'].iloc[0],
        'Last': df['last'].iloc[0],
        'TransCategory': df['category'].iloc[0],
        'State': df['state'].iloc[0]
    }
    
    # Saving row's index
    json_row_dir = os.path.join(os.path.dirname(__file__), '../wspace2/json')
    if not os.path.exists(json_row_dir):
        os.makedirs(json_row_dir)
    
    json_file = os.path.join(json_row_dir, 'row.json')
    df.to_json(json_file, orient='records')
    
    #print(specific_data)
    return json.dumps(specific_data)

if __name__ == '__main__':
    app.run()
