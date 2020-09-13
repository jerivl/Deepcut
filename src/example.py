'''
Example of code style desired

- Functions denoted with lowercase letters and underscores (funct_one)
- Classes denoted with uppercase letters and underscores (Class_One)
- Optimize code for readability


'''

def hello_world(int: x, int: y):
    print('hello world')
    return x + y

def main():
    z = 10
    for i in range(z):
        hello_world(i, z-i)

if __name__ == "__main__":
    main()
