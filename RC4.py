import argparse

STATE_SIZE = 256

def hex_to_bytes(string):
    return list(bytes.fromhex(string))

def bytes_to_hex(data):
    return bytes(data).hex().upper()

def text_to_bytes(string):
    return list(string.encode('utf-8'))

def bytes_to_text(data):
    return bytes(data).decode('utf-8')

def key_scheduling(key):
    if not key:
        raise ValueError("Key must not be empty")

    state = list(range(STATE_SIZE))
    j = 0
    for i in range(STATE_SIZE):
        j = (j + state[i] + key[i % len(key)]) % STATE_SIZE
        state[i], state[j] = state[j], state[i]
    return state

def keystream(state, length):
    i = j = 0
    stream = []
    for _ in range(length):
        i = (i + 1) % STATE_SIZE
        j = (j + state[i]) % STATE_SIZE
        state[i], state[j] = state[j], state[i]
        stream.append(state[(state[i] + state[j]) % STATE_SIZE])
    return stream

def xor(data1, data2):
    return [b1 ^ b2 for b1, b2 in zip(data1, data2)]

def crypt(method, key, input_data, output_data, text=False):
    to_bytes = text_to_bytes if text else hex_to_bytes
    key_bytes = to_bytes(key.read().strip())

    if text and method == 'dec':
        data = hex_to_bytes(input_data.read().strip())
    else:
        data = to_bytes(input_data.read().strip())

    state = key_scheduling(key_bytes)
    stream = keystream(state, len(data))
    result = xor(data, stream)

    if text and method == 'dec':
        return output_data.write(bytes_to_text(result))
    return output_data.write(bytes_to_hex(result))

def main():
    parser = argparse.ArgumentParser(description='RC4 Encryption')

    method_group = parser.add_mutually_exclusive_group(required=True)
    method_group.add_argument('--enc', action='store_const', dest='method', const='enc', help='Encryption method')
    method_group.add_argument('--dec', action='store_const', dest='method', const='dec', help='Decryption method')

    parser.add_argument('--text', action='store_true', help='Key and plaintext are plain text; ciphertext stays hex')
    parser.add_argument('key', type=argparse.FileType('r', encoding='utf-8-sig'), help='File contain the key (hex, or text with --text)')
    parser.add_argument('input', type=argparse.FileType('r', encoding='utf-8-sig'), help='File contain the input (hex, or text with --text on --enc)')
    parser.add_argument('output', type=argparse.FileType('w', encoding='utf-8'), help='File to write the output (hex, or text with --text on --dec)')

    args = parser.parse_args()

    crypt(args.method, args.key, args.input, args.output, args.text)

if __name__ == '__main__':
    main()
