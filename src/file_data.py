import sys
import os
import ast
from src.get_repo import get_github_file
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class File:
    """
    Represents a file under test from a GitHub repo

    Attributes:
        content (str): The file content
        methods (list[]): The method info extracted from the file
        prompts (list[]): The prompts generated based on method info

    Methods:
        display(): Print the data in the class
        extract_methods(): Search the node to find methods
        process_node_for_methods(node, class_name): Deal with each node
        prompting(k): Build prompts to ask LLM generating k assertions
    """
    def __init__(self, repo_owner, repo_name, file_path, branch, token=None):
        print("Getting the repo file...")
        self.content = get_github_file(repo_owner, repo_name, file_path, branch, token)
        self.methods = []
        self.prompts = []

    def display(self):
        print(self.content)
        for method in self.methods:
            if method['class']:
                print(f"Class '{method['class']}': {method['name']}")
            else:
                print(f"Func: {method['name']}")
            print(method['text'])
            print("\n" + "-" * 50 + "\n")

    def extract_methods(self):
        for node in ast.parse(self.content).body:
            self.process_node_for_methods(node)

    def process_node_for_methods(self, node, class_name=None):
        if isinstance(node, ast.FunctionDef):
            # Locate methods
            start_line = node.lineno - 1
            if hasattr(node.body[-1], 'end_lineno'):
                end_line = node.body[-1].end_lineno
            else:
                # Could lose some lines
                print("Warning: some lines of methods could be ignored.")
                end_line = node.body[-1].lineno

            # Get method lines
            method_lines = self.content.splitlines()[start_line:end_line]

            # Add indents
            indent = len(method_lines[0]) - len(method_lines[0].lstrip())
            method_text = '\n'.join(line[indent:] for line in method_lines)

            # Save method info
            self.methods.append({
                'name': node.name,
                'class': class_name,
                'text': method_text,
                'ast': node
            })

        # Deal with methods in classes
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                self.process_node_for_methods(child, node.name)

    def prompting(self, k=5, input_format="text", cot=False):
        messages = []
        for m in self.methods:
            prompt = f"""Generate test assertions for the Python function below. Adhere strictly to these requirements:

1. Output ONLY valid Python assert statements
2. Required format: `assert <expression>, "<optional_error_message>"`
3. Never include:
   - Explanations or comments
   - Code blocks (``` markers)
   - Function definitions
   - Natural language descriptions
   - Non-assert code

Positive Examples:
assert multiply(2, 3) == 6
assert add(5, -3) == 2, "Positive and negative addition"
with pytest.raises(ValueError):
    divide(10, 0)

Negative Examples (UNACCEPTABLE):
# Test case for multiply function
print(assert multiply(2,4))
"The result should be 8" 
def test_multiply():
    assert multiply(2,4) == 8

Now generate assertions for this function:"""
            if input_format == "ast":
                prompt += m['ast']
            else:
                prompt += m['text']
            if cot:
                prompt += "Let's think step by step:"
            messages.append(prompt)
        return messages

    def get_method_names(self):
        names = []
        for m in self.methods:
            names.append(m['name'])
        return names
