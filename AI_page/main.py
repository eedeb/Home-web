from flask import Flask, render_template, request, jsonify, render_template_string, make_response, send_from_directory
import Classy
import importlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api')
def api_home():
    return render_template('api.html')

@app.route('/api/<path:text>')
def api(text):
    text = text.replace('%20', ' ')
    x,y=Classy.classify(text,'/root/AI_page/static/data.pth')
    output = x+", "+str(y)
    return jsonify({"input": text,
                    "output": x,
                    "certainty": str(y)})




@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    api_key=request.form['api_key']
    #importlib.reload(Classy.New_ai)
    if request.cookies.get('key'):
        Classy.init('/root/AI_page/static/data.pth', request.cookies.get('key'))
        resp=make_response(jsonify({'status': 'success'}))
        resp.set_cookie('key',request.cookies.get('key'))
        api_key='cookie'
    else:
        api_key=request.form['api_key']
    if api_key == 'cookie':
        pass
    elif api_key == 'Custom1':
        Classy.init('/root/AI_page/static/data.pth','Custom API key 1')
        resp=make_response(jsonify({'status': 'success'}))
        resp.set_cookie('key','Custom API key 1')
    elif api_key == 'Custom2':
        Classy.init('/root/AI_page/static/data.pth','Custom API key 2')
        resp=make_response(jsonify({'status': 'success'}))
        resp.set_cookie('key','Custom API key 2')
    else:
        Classy.init('/root/AI_page/static/data.pth', api_key)
        resp=make_response(jsonify({'status': 'success'}))
        resp.set_cookie('key',api_key)
    return resp

@app.route('/get_response', methods=['POST'])
def get_response():
    cookie_key=request.cookies.get('key')
    Classy.init('/root/AI_page/static/data.pth',cookie_key)
    user_input = request.form['user_input']
    x, y, z, a = Classy.server(user_input)
    return jsonify({'response_1': x, 'response_2': y})

if __name__ == '__main__':
    app.run(debug=False, ssl_context=('fullchain.pem','privkey.pem'))
