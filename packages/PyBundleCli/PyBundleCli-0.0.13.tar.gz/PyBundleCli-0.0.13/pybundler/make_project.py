def make_project(project):
    with open(f'{project}.py', 'w') as f:
        f.write('''def main():
    print('Hello, world!')
''')
