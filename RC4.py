import argparse

STATE_SIZE = 256

def hex_to_bytes(string):
    """Convert a hex string to a list of byte values."""
    return list(bytes.fromhex(string))

def bytes_to_hex(data):
    """Convert a list of byte values to an uppercase hex string."""
    return bytes(data).hex().upper()

def key_scheduling(key):
    """KSA: build the initial permuted state array from the key."""
    if not key:
        raise ValueError("Key must not be empty")

    state = list(range(STATE_SIZE))
    j = 0
    for i in range(STATE_SIZE):
        j = (j + state[i] + key[i % len(key)]) % STATE_SIZE
        state[i], state[j] = state[j], state[i]
    return state

def keystream(state, length):
    """PRGA: generate `length` keystream bytes from the state array."""
    i = j = 0
    stream = []
    for _ in range(length):
        i = (i + 1) % STATE_SIZE
        j = (j + state[i]) % STATE_SIZE
        state[i], state[j] = state[j], state[i]
        stream.append(state[(state[i] + state[j]) % STATE_SIZE])
    return stream

def xor(data1, data2):
    """XOR two byte lists element by element."""
    return [b1 ^ b2 for b1, b2 in zip(data1, data2)]

def crypt(method, key, input_data, output_data):
    """Encrypt or decrypt hex input; RC4 applies the same operation for both."""
    key_bytes = hex_to_bytes(key.read().strip())
    data = hex_to_bytes(input_data.read().strip())

    state = key_scheduling(key_bytes)
    stream = keystream(state, len(data))

    return output_data.write(bytes_to_hex(xor(data, stream)))

def main():
    parser = argparse.ArgumentParser(description='RC4 Encryption')

    method_group = parser.add_mutually_exclusive_group(required=True)
    method_group.add_argument('--enc', action='store_const', dest='method', const='enc', help='Encryption method')
    method_group.add_argument('--dec', action='store_const', dest='method', const='dec', help='Decryption method')

    parser.add_argument('key', type=argparse.FileType('r'), help='File contain the key (hex)')
    parser.add_argument('input', type=argparse.FileType('r'), help='File contain the input (hex)')
    parser.add_argument('output', type=argparse.FileType('w'), help='File to write the output (hex)')

    args = parser.parse_args()

    crypt(args.method, args.key, args.input, args.output)

if __name__ == '__main__':
    main()
