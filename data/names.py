import random

vowels=['a', 'e', 'i', 'o', 'u', 'ae', 'ao', 'au', 'ei', 'eo', 'eu', 'ea', 'ee', 'io', 'ia', 'ua', 'ue', 'ui', 'uo', 'oa',
        'oe', 'oi', 'oy', 'oo', 'ay', 'ey', 'ù', 'è', 'ö', 'ä', 'ü', 'ì', 'à', 'ŭ', 'uh']
#通用辅音：
consos=['b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y', 'th', 'ch', 'sh', 'ph',
        'ly', 'lz','st', 'ty', 'ky', 'fy', 'dy', 'by', 'my', 'ny', 'sy', 'gy', 'zy', 'py', 'phy', 'hy', 'sk', 'sp', 'ĉ']
#不在结尾：
cap_con=['gh', 'sch', 'dh', 'kh', 'bh', 'br', 'pr', 'dr', 'wh', 'lr', 'fr', 'cr', 'gr', 'kr', 'tr', 'pl', 'bl',
         'cl', 'sl', 'str', 'fl']
#只在中间
mid_con=['pp', 'bb', 'tl', 'tt', 'gg', 'cc', 'dd', 'mm', 'dl', 'pch', 'psh','nm', 'cd', 'dc', 'sc', 'nstr', 'mstr',
          'shm', 'chm', 'rpr', 'ndl', 'nc', 'mc', 'rs', 'ls', 'rbl', 'mbl', 'nbl', 'lc', 'rv', 'lv', 'dg', 'xc']
#不在开头
end_con=[ 'mth', 'nth', 'gth', 'nch', 'mn', 'nt', 'rp', 'ng', 'ct', 'mp', 'lg', 'lt', 'rt', 'ss', 'll', 'ff', 'nn', 'nk', 'mk', 'rch',
          'kk', 'pt', 'gn', 'nd', 'rr', 'rn', 'rm', 'rl', 'thm', 'rb', 'mb', 'x', 'rk', 'rc', 'nf', 'rd']


def nameGen(l=3):
    name=[]
    start=random.randint(0,1)
    for i in range(l):
        if i%2==start:
            p=random.choice(vowels)
        else:
            if i==0:
                choice=random.choice([0,1])
                if choice:
                    p=random.choice(consos)
                else:
                    p=random.choice(cap_con)
            elif i==l-1:
                choice=random.choice([0,1])
                if choice:
                    p=random.choice(consos)
                else:
                    p=random.choice(end_con)
            else:
                choice=random.choice([0,1, 2, 3])
                if choice==0:
                    p=random.choice(consos)
                elif choice==1:
                    p=random.choice(cap_con)
                elif choice==2:
                    p=random.choice(mid_con)
                else:
                    p=random.choice(end_con)
        name.append(p)
    d=(''.join(name)).capitalize()
    print(d)

for i in range(100):
    length=random.randint(2, 3)
    nameGen(length)

    
                    
            


