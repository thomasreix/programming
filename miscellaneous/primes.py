#!/usr/bin/env python3
n = 10001
p = 0
primes = []
i = 1
total = 0
while p < n:
    prime = True
    i += 1
    for j in range(len(primes)):
        if i % primes[j] == 0:
            prime = False
            break
    if prime:
        primes.append(i)
        total += i
    p += 1
print(total)
