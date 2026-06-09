def process(data):
    from math import sqrt
    def is_prime(n): return n > 1 and all(n % i for i in range(2, int(sqrt(n)) + 1))
    new = {}
    for k, v in data.items():
        if isinstance(v, list):
            new[k] = sum(x for x in v if is_prime(x))
        else:
            new[k] = 1
            for x in v:
                if x % 2: new[k] *= x
    return new

data = {"A":[2,3,4,5,10],"B":(1,2,3,4,5),"C":[7,8,9],"D":(6,7,8)}
print(process(data))
