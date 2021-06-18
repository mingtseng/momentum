
m = []
blank = []
k = []
a = [["D1", "R1"], ["D1", "R2"], ["D2", "R1"], ["D3", "R1"], ["D3", "R2"], ["D4", "R1"]]
for row in a:
    if len(blank) == 0:
        blank.append(row[0])
        k.append(row)

    else:
        if blank[0] == row[0]:
            k.append(row)
            if a.index(row) == len(a) - 1:
                m.append(k)
        else:
            m.append(k)
            blank.pop()
            blank.append(row[0])
            k = []
            k.append(row)
            if a.index(row) == len(a) - 1:
                m.append(k)
print(m)

