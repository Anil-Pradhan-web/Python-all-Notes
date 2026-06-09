nums = [4,2,7,4,2,4,9,7,9,9]
unique = {n for n in nums}
freq = {n: nums.count(n) for n in unique}
sorted_nums = sorted(freq, key=lambda x: freq[x], reverse=True)
print("Unique:", unique)
print("Frequency:", freq)
print("Sorted by frequency:", sorted_nums)
