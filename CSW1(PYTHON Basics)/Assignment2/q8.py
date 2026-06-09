emails = ["test@gmail.com","hello123","abc.org","world@yahoo.com"]
valid = list(filter(lambda e: "@" in e and (e.endswith(".com") or e.endswith(".org")), emails))
domains = [e.split('@')[1].split('.')[0] for e in valid]
freq = {d: domains.count(d) for d in set(domains)}
print("Valid:", valid)
print("Domains:", domains)
print("Frequency:", freq)
