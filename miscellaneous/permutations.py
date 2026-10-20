def permute(items: list[int], lenth: int) -> list[list[int]]:
    if lenth == 0:
        return [[]]
    if lenth > len(items):
        return []
    permutations = []
    for i in range(len(items)):
        item = items[i]
        remaining = items[:i] + items[i + 1 :]
        current_permutations = permute(remaining, lenth - 1)
        for permutation in current_permutations:
            permutations.append([item] + permutation)
    return permutations


def main():
    items = [0, 1, 2, 3, 4]
    lenth = 3
    permutations = permute(items, lenth)
    print(f"There are {len(permutations)} permutations of length {lenth} from {items}")
    print(permutations)


if __name__ == "__main__":
    main()
