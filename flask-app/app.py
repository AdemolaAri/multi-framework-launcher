from flask import Flask, render_template, jsonify, request
import json
app = Flask(__name__, template_folder='templates', static_folder='static')
CONTENT = json.load(open('shared/content.json'))

@app.route('/')
def index():
    return render_template('index.html', content=CONTENT)

@app.route('/quiz/check', methods=['POST'])
def quiz_check():
    data = request.json
    answers = {'q1':'A','q2':'B','q3':'C'}
    score = sum(1 for k,v in data.items() if answers.get(k)==v)
    return jsonify({'score':score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
