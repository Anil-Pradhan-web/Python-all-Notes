import time, random

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time taken: {end - start:.2f} sec")
        return result
    return wrapper

@timer
def demo_func():
    dur = random.uniform(0.5, 1.5)
    print(f"Sleeping for {dur:.2f} sec")
    time.sleep(dur)

demo_func()
