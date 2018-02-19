import os


def load_file(name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources', name), 'r', encoding='utf-8') as f:
        return f.read()


def write_file(name, content):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources', name), 'w', encoding='utf-8') as f:
        f.write(content)
