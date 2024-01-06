from flask import Flask, request, jsonify, render_template
import generatefiles

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    print("generate design document pressed")
    content = request.json['content']
    result = generatefiles.generateDesignDocument(content)
    return jsonify(result)
    
@app.route('/generate_unit_tests', methods=['POST'])
def generate_unit_tests():
    print("generate unit tests pressed")
    content = request.get_json()['content']
    result = generatefiles.generateUnitTests(content)
    return jsonify(result)

@app.route('/generate_main_code', methods=['POST'])
def generate_main_code():
    print("generate main code pressed")
    data = request.get_json()
    markdown_content = data['markdown']
    code_content = data['code']
    output = generatefiles.generateMainCode(markdown_content, code_content)
    print(output)
    return jsonify(output=output)

if __name__ == '__main__':
    app.run(debug=True)