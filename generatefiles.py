# Import necessary libraries

# NOTE: You must change api_key.txt to your API key before running.
import openai
import os
import re
from openai import OpenAI
import sys
import traceback
import subprocess
from os.path import expanduser
    
# Function to safely load your OpenAI API key
def load_api_key():
    # replace this when committing to github
    key = open("api_key.txt").readline().strip()
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
Write Python code corresponding to the provided unit tests in a single file. 
Declare all variables correctly to ensure the code passes these tests. 
Exclude any modifications to the unit tests, focusing solely on the main code development.
'''
unit_test_prompt = '''
Write the unit tests of public functions in the following design, with detailed
explanation of what properties are tested. Put all the Python test code in one single file instead of many files.
Make sure calling unittest.main with
"unittest.main(argv=['first-arg-is-ignored'], exit=False)"
The main code is stored in mainCode.py instead of anything the design document would say. Import from mainCode.py for the main code instead of anywhere else.   
'''
debugging_prompt = '''
Identify the specific error message from the failed unit tests. 
Use this error message to explain what went wrong and diagnose the issue in the main code. 
Correct only the necessary parts of the main code, ensuring the error is resolved. 
Comment the file name at the start of the code block. 
Provide the complete main code output, including both the modified and unmodified sections.
If modifications are required in the unit test code, indicate this in a comment. 
Output the entire main code, highlighting the changes made to address the error message.

If unit test code needs to be fixed, state so in a comment. Output the entire main code regardless of which part needs to be changed.
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


def remove_markdown(input_string):
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
                file_content = section.split('\n', 1)[1]
            else:
                print("Unsupported file type encountered. starting:" + section.split('\n')[0])
                continue
            # Save the file to the current working directory
            return file_content

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
    
def generateUnitTests(design_doc):
    return remove_markdown(call_openAi_api(unit_test_prompt, design_doc))

def generateMainCode(design_doc, tests):
    return remove_markdown(call_openAi_api(main_code_prompt, "Here is the design:\n" + design_doc  + "\n\n\nAnd here are the unit tests:\n" + tests))

def runCode(code, tests):
    print("Executing unit tests:")
    process = subprocess.Popen(['python', expanduser("~") + "\\cache\\unitTests.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return [stdout, stderr]

def fixCode(code, tests, err):
    user_prompt =  "\n\n Main code is:\n" + code + "\n\n unit test code is:\n" + tests + "\n\n error encountered is:\n" + err
    fix = call_openAi_api(debugging_prompt,  user_prompt)
    return remove_markdown(fix)

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