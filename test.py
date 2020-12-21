import json

with open("./data/rr.json") as file:
    kek = json.load(file)

print(kek["1"]["1234"])

