from flask import Flask, render_template, request, jsonify
import Classy
import importlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    api_key = request.form['api_key']
    importlib.reload(Classy.New_ai)
    Classy.init('/root/AI_page/data.pth', api_key)
    return jsonify({'status': 'success'})

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    x, y, z, a = Classy.question(user_input)
    if 'https://www.google.com/search?q' in x:
        x = x.split('Adequate answer not found. Open ')[1]
    return jsonify({'response_1': x, 'response_2': y})

if __name__ == '__main__':
    app.run(debug=True, host="", port=80)
