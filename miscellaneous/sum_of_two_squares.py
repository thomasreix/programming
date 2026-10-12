from math import floor


def prime_factorization(n) -> list[tuple[int, int]]:
    limit = floor(n / 2)
    prime_factors = []
    exponent = 0
    diviser = 2
    divisible = True
    while divisible:
        if n % diviser == 0:
            n /= diviser
            exponent += 1
        elif diviser <= limit:
            if exponent > 0:
                factor = [diviser, exponent]
                prime_factors.append(factor)
            diviser += 1
            exponent = 0
        else:
            divisible = False

    if prime_factors == []:
        prime_factors = [(n, 1)]

    return prime_factors


def sum_of_two_squares(prime_factors: list[tuple[int, int]]):
    for factor in prime_factors:
        diviser = factor[0]
        if diviser % 4 == 3:
            exponant = factor[1]
            if exponant % 2 == 1:
                return False
    return True


n = 42
factors = prime_factorization(n)
print(factors)

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"  # Resets terminal back to default color

if sum_of_two_squares(factors):
    print(f"{GREEN}{n} can be expressed as the sum of two squares{RESET}")
else:
    print(f"{RED}{n} can't be expressed as the sum of two squares{RESET}")


expressable = 0
N = 1000
for n in range(N):
    n += 1
    factors = prime_factorization(n)
    if sum_of_two_squares(factors):
        expressable += 1

pourcentage = expressable / N * 100

print(
    f"there are {pourcentage}% of numbers from 1 to {N} that are expressable as the sum of two squares"
)
