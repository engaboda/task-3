import sympy


def generate_number(length):
    return sympy.randprime(2, 128)
