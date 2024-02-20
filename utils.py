import ast


def str_to_tuple(s):
    return ast.literal_eval(s)

def tuple_to_str(t):
    return str(t)
