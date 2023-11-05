from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# Ruta para cargar la página principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_purchase', methods=['POST'])
def save_purchase():
    data = request.get_json()
    json_data_directory = os.path.join(os.path.dirname(__file__), '../wspace2/json')
    print(json_data_directory)

    if not os.path.exists(json_data_directory):
        os.makedirs(json_data_directory)

    # Generate a unique filename for the JSON file
    file_name = os.path.join(json_data_directory, 'data.json')

    with open(file_name, 'w') as json_file:
        json.dump(data, json_file)
    
    return jsonify({'message': 'Data saved successfully'})

if __name__ == '__main__':
    app.run()
