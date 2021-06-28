import hashlib
import json


def crypto_hash(*args):
    """
    Return a sha-256 hash of the given arguments.
    """

    str_args = [json.dumps(arg) for arg in args]

    joined_data = "^".join(str_args)

    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()


def main():
    print(f"crypto_hash(1): {crypto_hash('foo', [12, 13], 'sobaka', 15)}")
    print(f"crypto_hash(2): {crypto_hash('foo',  'sobaka', [12, 13], 15)}")


if __name__ == "__main__":
    main()
