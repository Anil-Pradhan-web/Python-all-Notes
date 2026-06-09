import re

def filter_emails(lst):
    result = []
    pattern = r'^[A-Za-z0-9][A-Za-z0-9._]*@[A-Za-z]+\.[A-Za-z]{2,4}$'

    for email in lst:
        if re.match(pattern, email):
            result.append(email)
    return result

# Test
lst = ["student123@gmail.com", "teacher.name@soa.edu", "abc.xyz@abc.in",
       "xyz#12@abc.com", "bad@1n.com"]

print(filter_emails(lst))
