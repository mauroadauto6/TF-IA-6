from flask import Flask, render_template, Response, send_from_directory
import json
import os
import time

app = Flask(__name__)

json_folder = os.path.join(os.path.dirname(__file__), 'json')
print(json_folder)

def get_latest_json():
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    if json_files:
        latest_json = max(json_files, key=lambda x: os.path.getctime(os.path.join(json_folder, x)))
        with open(os.path.join(json_folder, latest_json), 'r') as archivo_json:
            return json.load(archivo_json)
    return None

def generate_events():
    last_json = None
    print('EVENT')
    while True:
        data = get_latest_json()
        if data and data.get('is_fraud') == 1:
            if data != last_json:
                last_json = data
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