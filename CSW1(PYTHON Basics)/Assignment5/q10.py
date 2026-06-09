import pickle

data = {"Alice": (20, "A"), "Bob": (19, "B"), "Charlie": (21, "A")}

with open("students.pkl", "wb") as f:
    pickle.dump(data, f)

print("Pickled data saved successfully.")

with open("students.pkl", "rb") as f:
    loaded_data = pickle.load(f)

print("Unpickled data:", loaded_data)
