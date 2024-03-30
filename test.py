from functools import wraps
from typing import Callable
def say_wrapper(method: Callable):
    @wraps(method)
    def wrapper(*args, **kwargs):
        print("I am a wrapper")
        return method(*args, **kwargs)
    return wrapper


def count_calls(fn):
    method_n = fn.__qualname__
    count = 0
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    print(method_n)
    return wrapper

@count_calls
@say_wrapper
def say_hello():
    return "hello ninja"


print(say_hello())
