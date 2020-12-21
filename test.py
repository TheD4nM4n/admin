import json

with open("./config/rr.json") as file:
    kek = json.load(file)

print(kek["1"]["1234"])

