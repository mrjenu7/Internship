# --------------- Dictionary : ----------------

mydict = {
    "one" : 1,
    "two" : 2,
    3 : "three",
    4.5 : ["four", "point", "five"]
}
#print(mydict["one"])

#mydict["five"] = 5
#print(mydict)

#print(mydict.keys())
#print(mydict.values())

for key, val in mydict.items():
    print(key, val)