# repo_tester
This is a Python program that generates and runs tests for a Python program file in a given GitHub repo. 
It takes the program's git repository and the relative path to the file as input. 
It generates a test file containing one test method per source-code method in the given file.

## Install
Clone this repo and install all dependencies.
```
git clone https://github.com/IIllIlllIl/repo_tester.git

pip install -r requirement.txt
```
Then, this program uses LLM to generate test assertions. Therefore, to run this program, a llm server API is required.
We recommend using vllm(https://github.com/vllm-project/vllm) to build a local LLM API server. 
The tool Vllm can be downloaded and set according to their documents.

## Usage
To understand this program, We provide an example of this program. The program under test in the example is a python 
program "ciphers/base32.py" in the GitHub repo: https://github.com/TheAlgorithms/Python.git.

### Example
Before running the test, we should first start the LLM server. In the example, we use the model, 
"deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", downloaded from Huggingface(https://huggingface.co/). 
You can use your own LLM models or API instead.

Run the LLM server:
```
python -m vllm.entrypoints.openai.api_server --model "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
```

After starting the LLM server, we can run this program. If you are using your own LLM models or API, make sure you have
change the configuration JSON file, "example/config.json". 


Run the program:
```
python cmd_tester.py
```

### Test other repositories
If you want to test another Python file, you should first change the configurations. In the configuration, you should 
change the repo info ("repo_owner", "repo_name", "branch", "token") and 
LLM API info ("based_url", "relative_url", "temperature").

Then, you have to make sure all dependencies of the GitHub repo are installed. If some specific packages are expected 
to be imported in the test file, add them into the configuration file ("imports").

A configuration file contains:
- repo_owner: The owner of the GitHub repo.
- repo_name: The name of the GitHub repo.
- branch: The targeted branch in the GitHub repo.
- token: GitHub token.
- output: The local path where the repo should be cloned.
- based_url: The based URL of the LLM API.
- relative_url: The relative URL of the LLM API.
- model: The name of the LLM model.
- imports: The models should be imported in the test file.
- temperature: The temperature input for the LLM model.

After starting your own LLM server, you can this program with your own configuration:
```
python cmd_tester.py - c <path/to/config> -k <maximun number of assertions for each method under test>
```

## Modification
If you want to write your own program based on this program, here are some detailed designs for better understanding.

### Files
Here list of the model files involved in the program flow:

- cmd_tester: It deals with the cmd input and calls other models accordingly.
- config: It reads attributes from the configuration JSON file.
- reader: It deals with files, including reading, writing, creating, and deleting.
- get_repo: It gets the file content of the file under test, and clones the GitHub repo.
- file_date: It analyzes the file content, extracts methods, and functions, and creates LLM prompts.
- generator: It first checks whether the assertions from LLM can pass the compilation.
Includes all test assertions.
- model: It calls the LLM API to get assertions.
- dependency: It extracts imported packages from the original file.
- build file: It creates a test file with assertions passed compilation.

### Flow
By running the cmd_tester, it will
1) process the cmd args
2) get the repo file and clone the repo
3) generate LLM prompts according to the file
4) call LLM API to generate assertions
5) check assertions if they can pass compilation
6) build a test file with passed assertion

### Prompting
This program currently provides two options for prompting. 
The Python method "prompting" in "file_data" builds the prompt:
```python
def prompting(self, k=5, input_format="text", cot=False):
    messages = []
    for m in self.methods:
        prompt = f"""You are a professional Python test engineer.
        Please generate at least {k} test assertions for the following Python methods. 
        Requirements:
        1. analyze the method's input parameters, return values, and possible behaviors
        2. generate assertions for multiple typical test scenarios, 
        including normal case, boundary case, and abnormal case
        3. use pytest style `assert` statements
        4. Do not generate the actual test code or explanations, only the assertions.
        Method information:"""
        if input_format == "ast":
            prompt += m['ast']
        else:
            prompt += m['text']
        if cot:
            prompt += "Let's think step by step:"
        messages.append(prompt)
    return messages
```
- input_format: choose to provide ast or source code
- cot: use the chain of thought technique or not
