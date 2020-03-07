import json

lst=[]

for i in range(1, 5):
    single = []
    for j in range(7):
        name = input("Name of an attribute: ")
        tem = [name, 0, 0, 0, 0, 0, 0]
        tem[i] = j - 1
        single.append(tuple(tem))
    lst.append(single)

lst.append([("Ripped", -1, -1, 0, 0, 0, 0), ("Fighter", 1, 1, 0, 0, 0, 0), ("Focused", 2, 2, 0, 0, 0, 0),
        ("Prudent", 3, 3, 0, 0, 0, 0)])
lst.append([("Rushed", -1, 0, 0, -1, 0, 0), ("Cavalry", 1, 0, 0, 1, 0, 0), ("Berserk", 2, 0, 0, 2, 0, 0),
        ("Zealous", 3, 0, 0, 3, 0, 0)])
lst.append([("Vulnerable", 0, -1, 0, -1, 0, 0), ("Calm", 0, 1, 0, 1, 0, 0), ("Veteran", 0, 2, 0, 2, 0, 0),
        ("Aquatic", 0, 3, 0, 3, 0, 0)])
lst.append([("Accursed", 0, -1, -1, 0, 0, 0), ("Pious", 0, 1, 1, 0, 0, 0), ("Azure", 0, 2, 2, 0, 0, 0),
        ("Divine", 0, 3, 3, 0, 0, 0)])
lst.append([("Ignorant", 0, 0, -1, -1, 0, 0), ("Voilet", 0, 0, 1, 1, 0, 0), ("Unearthly", 0, 0, 2, 2, 0, 0),
        ("Windy", 0, 0, 3, 3, 0, 0)])
lst.append([("Gifted", 0, 1, 1, 1, 0, 0), ("Universal", 1, 1, 0, 1, 0, 0), ("Grandmaster", 1, 1, 1, 2, 0, 0),
        ("Saturated", 1, 2, 1, 2, 0, 0), ("Mysterious", 0, 2, 2, 2, 0, 0), ("Dominating", 3, 2, 0, 3, 0, 0),
        ("Emperor", 0, 2, 3, 2, 0, 0), ("Rusty", -1, -1, -1, -1, 0, 0)])
lst.append([("Scortching", 1, 0, 0, 0, 0, 1), ("Boreal", 1, 0, 0, 0, 0, 2), ("Noxious", 1, 0, 0, 0, 0, 3),
         ("Blinding", -1, 0, -1, 0, 0, 4), ("Expensive", 0, 0, 0, 0, 0, 5), ("Burdensome", 0, 0, 0, 0, 0, 6),
         ("Luminous", 0, 0, 1, 0, 0, 7)])

with open("new_attr.json", 'w') as wri:
    json.dump(lst, wri)
