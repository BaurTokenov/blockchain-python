from backend.util.crypto_hash import crypto_hash

HEX_TO_BINARY_TABLE = {}

for i in range(16):
    hex_digit = hex(i)[2:]
    binary_len = 4
    binary_digit = bin(i)[2:]
    binary_digit = (binary_len - len(binary_digit)) * "0" + binary_digit

    HEX_TO_BINARY_TABLE[hex_digit] = binary_digit

print(HEX_TO_BINARY_TABLE)


def hex_to_binary(hex_string):
    binary_string = ""

    for character in hex_string:
        binary_string += HEX_TO_BINARY_TABLE[character]

    return binary_string


def main():

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash("sobaka"))
    print(hex_to_binary_crypto_hash)


if __name__ == "__main__":
    main()
