def classify(nums):
    from math import sqrt
    def is_prime(n): return n > 1 and all(n % i for i in range(2, int(sqrt(n)) + 1))
    d = {"Prime": [], "Composite": [], "Perfect Squares": [], "Perfect Cubes": []}
    for n in nums:
        if is_prime(n): d["Prime"].append(n)
        elif n > 1: d["Composite"].append(n)
        if int(sqrt(n))**2 == n: d["Perfect Squares"].append(n)
        if round(n ** (1/3)) ** 3 == n: d["Perfect Cubes"].append(n)
    return d

nums = [2, 4, 8, 9, 27, 28]
print(classify(nums))
