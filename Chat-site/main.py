from flask import Flask, render_template, request, jsonify
import CustomChat

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    user_ip = request.remote_addr  # Get the user's IP address
    if user_input == 'reset':
        CustomChat.reset(user_ip)
        return jsonify({'response_1': 'reset', 'response_2': ''})
    else:
        responses = CustomChat.get_response(user_input, user_ip)  # Pass the user's IP address to get_response
        return jsonify({'response_1': responses[0], 'response_2': responses[1]})

if __name__ == '__main__':
    app.run(debug=True, host="172.235.133.234", port=80)
