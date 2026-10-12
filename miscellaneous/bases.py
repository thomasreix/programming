def decimal_to_binary(number: int) -> str:
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number //= 2
    return binary


def binary_to_decimal(binary: str) -> int:
    number = 0
    power = 2 ** len(binary)
    for bit in binary:
        power //= 2
        number += int(bit) * power
    return number


def decimal_to_byte(decimal: int) -> int:
    if not 0 <= decimal <= 255:
        return "invalid"

    byte = decimal_to_binary(decimal)
    return byte


def opposite_byte(binary: str) -> str:
    if len(binary) != 8:
        return "invalid"

    opposite = ""
    for bit in binary:
        opposite += str(1 - int(bit))

    return opposite


def main():
    decimal_1 = 648
    binary_1 = decimal_to_binary(decimal_1)
    print(f"{decimal_1} in binary is {binary_1}")

    binary_2 = "110110011101"
    decimal_2 = binary_to_decimal(binary_2)
    print(f"{binary_2} in decimal is {decimal_2}")

    decimal_3 = 190
    byte_3 = decimal_to_byte(decimal_3)
    print(f"{decimal_3} in 8 bit binary is {byte_3}")

    byte_4 = "10011000"
    opposite_byte_4 = opposite_byte(byte_4)
    print(f"the opposite of {byte_4} is {opposite_byte_4}")


if __name__ == "__main__":
    main()
