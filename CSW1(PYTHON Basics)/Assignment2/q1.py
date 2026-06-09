scores = [56, 78, 90, 45, 88, 67]
avg = sum(scores) / len(scores)
print("Average:", avg)
print("Min:", min(scores), "Max:", max(scores))
print("Above Average:", [s for s in scores if s > avg])
scores.sort(reverse=True)
print("Descending:", scores)
scores[-3:] = [0, 0, 0]
print("After replacing lowest 3 with 0:", scores)
