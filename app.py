from flask import Flask, request, jsonify, render_template
import generatefiles
from os import path, makedirs

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

@app.route('/run_main_code', methods=['POST'])
def run_code():
    print("run main code pressed")
    data = request.get_json()
    tests = data['tests']
    code = data['code']
    result = generatefiles.runCode(code, tests)
    print(result[1])
    error = result[1].decode('utf-8').replace('\\n', '\n').replace('\\\'', '\'')
    return jsonify(output=error)

@app.route('/debug_with_error', methods=['POST'])
def debug_code():
    print("debug pressed")
    data = request.get_json()
    tests = data['tests']
    code = data['code']
    err = data['error']
    result = generatefiles.fixCode(code, tests, err)
    print(result)
    return jsonify(output=result)

@app.route('/save_content', methods=['POST'])
def save_content():
    home = path.expanduser("~")
    cache_dir = path.join(home, 'cache')

    makedirs(cache_dir, exist_ok=True)

    data = request.get_json()

    # Save the content to a file
    with open(path.join(cache_dir, 'markdown1.txt'), 'w') as file:
        file.write(data['markdown1'])
    with open(path.join(cache_dir, 'markdown2.txt'), 'w') as file:
        file.write(data['markdown2'])
    with open(path.join(cache_dir, 'unitTests.py'), 'w') as file:
        file.write(data['code1'])
    with open(path.join(cache_dir, 'mainCode.py'), 'w') as file:
        file.write(data['code2'])
    return jsonify({"status": "success", "message": "Content saved successfully"})

@app.route('/get_cache', methods=['GET'])
def get_cache():
    home = path.expanduser("~")
    cache_dir = path.join(home, 'cache')

    # Create the cache directory if it doesn't exist
    makedirs(cache_dir, exist_ok=True)

    markdown1, markdown2, code1, code2 = "", "", "", ""
    try:
        with open(path.join(cache_dir, 'markdown1.txt'), 'r') as file:
            markdown1 = file.read()
    except IOError:
        markdown1 = "Write your program description here"

    try:
        with open(path.join(cache_dir, 'markdown2.txt'), 'r') as file:
            markdown2 = file.read()
    except IOError:
        markdown2 = "Design document will appear here"

    try:
        with open(path.join(cache_dir, 'unitTests.py'), 'r') as file:
            code1 = file.read()
    except IOError:
        code1 = "Unit tests will appear here"

    try:
        with open(path.join(cache_dir, 'mainCode.py'), 'r') as file:
            code2 = file.read()
    except IOError:
        code2 = "Main code will appear here"
    return jsonify({"status": "success", "markdown1": markdown1, "markdown2": markdown2, "code1": code1, "code2": code2})
if __name__ == '__main__':
    app.run(debug=True)