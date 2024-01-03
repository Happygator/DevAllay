from flask import Flask, request, jsonify, render_template
import generatefiles

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    content = request.json['content']
    result = generatefiles.generateDesignDocument(content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)