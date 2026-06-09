voters = [("Amit",22,"Indian"),("John",30,"USA"),("Neha",17,"Indian"),("Ravi",19,"Indian")]
eligible = list(filter(lambda x: x[1] >= 18 and x[2] == "Indian", voters))
not_eligible = [v for v in voters if v not in eligible]
print("Eligible:", [v[0] for v in eligible])
print("Count:", len(eligible))
print({"Eligible":[v[0] for v in eligible],"Not Eligible":[v[0] for v in not_eligible]})
