def decimal_to_binary(number: int) -> str:
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number //= 2

    return binary


def binary_to_decimal(binary: str) -> int:
    decimal = 0

    for i, bit in enumerate(reversed(binary)):
        decimal += int(bit) * (2**i)

    return decimal


def decimal_to_byte(number: int) -> str:
    if not 0 <= number <= 255:
        return ""

    binary = decimal_to_binary(number)
    return binary.zfill(8)


def byte_opposite(binary: str) -> str:
    if len(binary) != 8:
        return ""

    opposite = ""

    for bit in binary:
        opposite += "1" if bit == "0" else "0"

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
    print(f"{decimal_3} in 8-bit binary is {byte_3}")

    byte_4 = "10011000"
    opposite_byte_4 = byte_opposite(byte_4)
    print(f"The opposite of {byte_4} is {opposite_byte_4}")


if __name__ == "__main__":
    main()
