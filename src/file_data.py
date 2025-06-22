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
        prompting(): Build prompts to ask LLM
        get_method_names(): Get all method names in the file under test
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

    def prompting(self, model_name, input_format="text", cot=False):
        messages = []
        for m in self.methods:
            prompt = """Generate Python unit test code strictly following these requirements:
1. **Output Format**: Wrap the entire code in a Markdown Python code block (```python ... ```)
2. **Testing Framework**: Use pytest (not unittest) and only import pytest
3. **Test Organization**:
   - Structure tests as ONE function (no test classes)
   - Group by scenario in one function:
     ```python
     def test_{function_name}:
        # Normal cases
        ...
        # Edge/boundary cases
        ...
        # Error/exception cases
        ...
     ```
4. **Type Safety**:
   - All test parameters must match the function's type annotations
   - Validate type errors using `pytest.raises(TypeError)`
   - Include parameterized tests where appropriate
5. **Complete Structure**:
   ```python
   # Function under test (include definition)
   def target_function(...): ...
   
   # ===== Test cases  =====
   import pytest
   
   def test_{function_name}():
        # Normal cases
        ...
        # Edge/boundary cases
        ...
        # Error/exception cases
        ...
6. Purity: Output ONLY the Markdown code block with no additional text."""
            prompt += f"Function to test in model {model_name}:"
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
