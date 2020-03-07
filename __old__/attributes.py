import json
dct2=[(-1, ['Normal', 0, 0, 0, 0, 0, 0]), (0, ['Ordinary', 0, 0, 0, 0, 0, 0]), (1, ['Broken', -2, -1, -1, -2, 0, -0.3]), (2, ['Rusty', -1, 0, 0, 0, 0, -0.2]), (3, ['Fragile', 0, -1, 0, 0, 0, -0.2]),
      (4, ['Ignorant', 0, 0, -1, 0, 0, -0.2]), (5, ['Blunt', 0, 0, 0, -1, 0, -0.2]), (6, ['Expensive', 0, 0, 0, 0, 0, 1]), (7, ['Heavy', 0, 0, 0, 0, 1, -0.2]), (8, ['Sharp', 1, 0, 0, 0, 0, 0.3]),
      (9, ['Hard', 0, 1, 0, 0, 0, 0.3]), (10, ['Shining', 0, 0, 1, 0, 0, 0.3]), (11, ['Light', 0, 0, 0, 1, 0, 0.3]), (12, ['Fatal', 2, 0, 0, 0, 0, 0.8]), (13, ['Defensive', 0, 2, 0, 0, 0, 0.8]),
      (14, ['Magical', 0, 0, 2, 0, 0, 0.8]), (15, ['Rapid', 0, 0, 0, 2, 0, 0.8]), (16, ['Fighter\'s', 3, 1, 0, 0, 0, 1.2]), (17, ['Guardian\'s', 0, 3, 0, 1, 0, 1.2]), (18, ['Wizard\'s', 0, 0, 3, 1, 0, 1.2]), 
      (19, ['Ninja\'s', 1, 0, 0, 3, 0, 1,2]), (20, ['Colorful', 0, 1, 1, 1, 0, 1.4]), (21, ['Universal', 2, 1, 1, 1, 0, 1.5]), (22, ['Eviscerate', 4, 0, 0, 1, 0, 1.8]), (23, ['Rocky', 0, 5, 0, 0, 0, 1.8]),
      (24, ['Mysterious', -1, 1, 4, 1, 0, 1.8]), (25, ['Spider', 1, 0, 0, 4, 0, 1.8]), (26, ['Saturated', 4, 1, 0, 1, 0, 2]),(27, ['Gifted', -1, 2, 4, 1, 0, 2]), (28, ['Divine', 1, 1, 1, 3, 0, 2]),
      (29, ['Berserk', 5, 0, 0, 1, 0, 2.2]),(30, ['Undead', 0, 4, 0, 2, 0, 2.2]), (31, ['Spiritual', 0, 0, 0, 6, 0, 2.2]), (32, ['Windy', 0, 1, 0, 5, 0, 2.2]), (33, ['Dominated', 4, 2, 1, 1, 0, 3]),
      (34, ['Pervasive', 2, 2, 2, 2, 0, 3]),(35, ['Storm', 1, 2, 1, 6, 0, 4]), (36, ['Volcano', 6, 2, 0, 2, 0, 4]), (37, ['Unexisted', 0, 2, 6, 2, 0, 4]), (100, ['Lvl6_1', 1, 2, 1, 2, 0, 1]),
      (101, ['Lvl6_2', 0, 2, 2, 2, 0, 1]), (102, ['Lvl6_3', 2, 2, 0, 2, 0, 1]), (103, ['Lvl6_4', 3, 2, 1, 2, 0, 1]), (104, ['Lvl6_5', 1, 2, 1, 3, 0, 1]), (105, ['Lvl6_6', 1, 2, 3, 2, 0, 1])]

with open('attributes.json', 'w') as w:
    json.dump(dict(dct2), w)

