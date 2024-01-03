# Import necessary libraries

# NOTE: You must change api_key.txt to your API key before running.
import openai
import os
import re
from openai import OpenAI
import sys
import traceback
import subprocess
    
# Function to safely load your OpenAI API key
def load_api_key():
    # replace this when committing to github
    key = open("api_key.txt").readline()
    return key

# Initialize OpenAI SDK
openai.api_key = load_api_key()
client = OpenAI(
    api_key= load_api_key(),
)

design_doc_prompt = '''
Convert the following program requirements to a more detailed design document in markdown format.
Assume all code will be in a single module.
List the public functions needed, but do not write their code.
Format your output entirely in plain English, with no code written yet. We need to first go over the design document.
 The requirements start below this line:
 -------------------------------------
'''

main_code_prompt = '''
Implement the Python code for the design and the unit tests in one single file.
Make sure all variables are propertly declared and the code should pass all the unit tests.
Before each file, explicitly write a filename.
'''
unit_test_prompt = '''
Write the unit tests of public functions in the following design, with detailed
explanation of what properties are tested. Put all the Python test code in one single file instead of many files.
Make sure calling unittest.main with
"unittest.main(argv=['first-arg-is-ignored'], exit=False)"

Also generate HTML files needed for testing.
output all Python code file and HTML files one by one preceded with their filename:
'''
debugging_prompt = '''
The execution of the unit tests has failed.
Explain what went wrong, then fix the entire main code including the part that doesn't need to be changed.
Put file name code in the code block as a comment.
Output the entire main code afterwards, including every section that was unchanged.
Do not write anything similar to (other functions remain unchanged). Instead, simply write the rest of the unchanged code.

If unit test code needs to be fixed, ouput the entire unit test code including the part that doesn't need to be changed.
'''
valid_inputs = ["y", "n", ""]

spec = open("spec.txt").read()

def prompt_continue():
    userinput = "d"
    while userinput.lower() not in valid_inputs:
        userinput = input("Continue? (Y/n)")
    if userinput.lower() == "n":
        sys.exit()

def call_openAi_api(system_prompt, user_input):
    """ Call OpenAI """
    try:
        response = client.chat.completions.create(
            messages=[{
              "role": "system",
              "content":system_prompt,
              },
              {
              "role": "user",
              "content":user_input,
            }],
            # model = "gpt-4"
            model = "gpt-3.5-turbo-1106",
            temperature = 0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'Error: {str(e)}'       
        

def clean(code):
  lines = code.split('\n')
  lines = '\n'.join(lines[1:-1])
  lines = remove_markdown(lines)
  return lines

def remove_markdown(code):
  return code.replace("```python", "").replace("```", "")

def save_files_from_string(input_string):
    file_names = []
    # Split the input string by triple backticks
    file_sections = input_string.split('```')
    print('sections')
    for s in file_sections:
      print(s.split('\n')[0])
    print('/sections')

    for section in file_sections:
        if section.strip():  # Check if the section is not empty
            # Identify file type
            if section.lower().startswith('python'):
                # Extract file name, which might be preceded by a # sign
                file_name = re.search(r'#?(.+\.py)', section).group(1).strip()
                # Extract file content
                file_content = section.split('\n', 1)[1]
            elif section.lower().startswith('html'):
                # Extract file name from HTML comment
                file_name = re.search(r'<!--\s*(.+\.html)\s*-->', section).group(1).strip()
                # Extract file content
                file_content = section.split('\n', 1)[1]
            else:
                print("Unsupported file type encountered. starting:" + section.split('\n')[0])
                continue
            file_name = "generated_files\\" + file_name
            # Save the file to the current working directory
            with open(os.path.join(os.getcwd(), file_name), 'w') as file:
                file.write(file_content)
                file_names.append(file_name)
    return file_names

def generateDesignDocument(spec):
    return call_openAi_api(design_doc_prompt, spec)
"""
design = call_openAi_api(design_doc_prompt, spec)
print("This is the design document created:")
print(design)

prompt_continue()

unit_tests = (call_openAi_api(unit_test_prompt, design))
print("\n\n Unit Tests: \n \n")
print(unit_tests)
tests = save_files_from_string(unit_tests)

prompt_continue()

print("\n\nMain Code \n\n")
main_code = call_openAi_api(main_code_prompt, "Here is the design:\n" +design + "\n\n\nAnd here are the unit tests:\n" + unit_tests)
print(main_code)
code = save_files_from_string(main_code)



outfile = open("main.py", "w")
outfile.write(main_code)
outfile.close()
continue_testing = True
while continue_testing:
    prompt_continue()
    print("Executing unit tests:")
    process = subprocess.Popen(['python', tests[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print('======')
    print(stderr.decode("utf-8"))
    prompt_continue()
    user_prompt =  "The file name for the main code is " + code[0] + "\n\n main code is:\n" + open(code[0]).read() + "The file name for unit tests is " + tests[0] + "\n\n unit test code is:\n" + open(tests[0]).read() + "\n\n error encountered is:\n" + stderr.decode("utf-8")
    fix = call_openAi_api(debugging_prompt,  user_prompt)
    save_files_from_string(fix)
    print(fix)
"""