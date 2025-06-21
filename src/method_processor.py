class Method:
    """
        Abandoned class
    """
    def __init__(self, method_name, method_class, method_content):
        self.name = method_name
        self.m_class = method_class
        self.content = method_content

    def display(self):
        print(self.name)
        print(self.content)
