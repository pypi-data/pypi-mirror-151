
def make_init():
    template = """__VERSION__ = '0.0.1'
"""
    with open('__init__.py', 'w') as f:
        f.write(template)
