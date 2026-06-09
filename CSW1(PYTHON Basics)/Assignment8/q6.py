import numpy as np

def generate_data():
    data = np.random.randn(1000)
    mean = np.mean(data)
    std = np.std(data)
    return data, mean, std

def analyze_distribution(data, mean, std):
    result = {}
    result["1_std"] = np.sum((data >= mean-std) & (data <= mean+std))
    result["2_std"] = np.sum((data >= mean-2*std) & (data <= mean+2*std))
    result["3_std"] = np.sum((data >= mean-3*std) & (data <= mean+3*std))
    return result

data, mean, std = generate_data()
dist = analyze_distribution(data, mean, std)

print(dist)
