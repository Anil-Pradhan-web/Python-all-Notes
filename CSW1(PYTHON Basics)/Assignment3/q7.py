import random

def sensor_data_stream():
    while True:
        yield round(random.uniform(20, 30), 2)

gen = sensor_data_stream()
for _ in range(10):
    print(next(gen))
