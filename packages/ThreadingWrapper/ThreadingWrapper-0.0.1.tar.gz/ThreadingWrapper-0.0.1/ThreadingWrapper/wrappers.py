import time


def time_it(function_name: str = None):
    def decorator(func):
        def inner(*args, **kwargs):
            begin = time.time()
            print(f"Executing: {function_name if function_name is not None else func.__name__}")
            output = func(*args, **kwargs)
            end = time.time()
            print(f"Completed: {function_name if function_name is not None else func.__name__}, in {end - begin}")
            return output
        return inner
    return decorator
