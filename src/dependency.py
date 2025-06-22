import ast
from typing import List, Set


class Dependency:
    """
    Get all packages from file under test

    Attributes:
        test_file_content (str): The content of file under test
        additional_imports (List): Additional packages from configuration file
        tree (ast): The ast of the file under test

    Methods:
        extract_existing_imports(): Get all packages of file under test
        extract_additional_imports(): Get all additional packages from configuration file
        generate_imports(): Generate packages import lines
        path_to_import(path): Change file under test path into import format
    """
    def __init__(self, test_file_content, additional_imports=None):
        self.test_file_content = test_file_content
        self.additional_imports = additional_imports or []
        self.tree = ast.parse(test_file_content)

    def extract_existing_imports(self):
        existing_imports = []
        for node in self.tree.body:
            if isinstance(node, ast.Import):
                # Deal with "import"
                modules = [alias.name for alias in node.names]
                existing_imports.append(f"import {', '.join(modules)}")
            elif isinstance(node, ast.ImportFrom):
                # Deal with "from import"
                if node.module:
                    names = [alias.name for alias in node.names]
                    existing_imports.append(f"from {node.module} import {', '.join(names)}")

        return existing_imports

    def extract_additional_imports(self):
        additional_imports = set()
        for imp in self.additional_imports:
            if imp.startswith("from "):
                additional_imports.add(imp)
            else:
                additional_imports.add(f"{imp}")

        return additional_imports

    def generate_imports(self):
        existing_imports = self.extract_existing_imports()
        additional_imports = self.extract_additional_imports()
        all_imports = existing_imports + list(additional_imports - set(existing_imports))
        return "\n".join(all_imports)

    @staticmethod
    def path_to_import(path):
        components = []
        for part in path.split('/'):
            part = part.strip()
            if part:
                if '.' in part and not part.startswith('.'):  # 排除隐藏文件
                    part = part.rsplit('.', 1)[0]
                components.append(part)
        result = '.'.join(components)
        return result.lstrip('.')
