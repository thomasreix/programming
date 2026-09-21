n = 100
lf = 0
m = 0
f = 0
while lf < n:
    m += 1
    f = (m * (m + 1)) / 2
    factor = [1]
    j = 2
    i = f
    while i > j:
        if i % j == 0:
            factor.append(j)
        j += 1
    lf = len(factor)
print(f)
