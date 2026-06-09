students = {"Ram":[85,90,92],"Laxman":[70,80,88],"Janaki":[95,100,90]}
avg = {name: sum(scores)/len(scores) for name, scores in students.items()}
top = max(avg, key=avg.get)
print("Top Student:", top)
