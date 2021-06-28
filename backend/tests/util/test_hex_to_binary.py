from backend.util.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    original_number = 7861
    hex_number = hex(original_number)[2:]
    bin_number = hex_to_binary(hex_number)

    assert int(bin_number, 2) == original_number
