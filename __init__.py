import pytest
import subprocess

@pytest.mark.skip(reason="This is a decorator")
def test(name, score):
    def decorator(func):
        func.test = True
        func.test_name = name
        func.test_score = score
        func = pytest.mark.timeout(30)(func)
        return func
    return decorator

def run(*args):
    return subprocess.check_output(args).decode("utf-8").strip()