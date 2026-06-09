students = [
    {"info": (1,"Ram"), "marks": [85,90,95], "skills": {"Python","Java"}},
    {"info": (2,"Sita"), "marks": [75,80,70], "skills": {"Python","C"}},
    {"info": (3,"Laxman"), "marks": [90,88,92], "skills": {"C","Java"}}
]

avg_marks = {s["info"][1]: sum(s["marks"])/len(s["marks"]) for s in students}
skill_freq = {}
for s in students:
    for skill in s["skills"]:
        skill_freq[skill] = skill_freq.get(skill,0) + 1
top = max(avg_marks, key=avg_marks.get)

print("Average Marks:", avg_marks)
print("Skill Frequency:", skill_freq)
print("Top Student:", top)
