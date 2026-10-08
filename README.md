# Modul RC4 (Rivest Cipher 4)

RC4 is a symmetric-key **stream cipher** designed by Ron Rivest in 1987. Unlike DES, it does not process fixed-size blocks; it generates a pseudo-random keystream and XORs it with the data byte by byte.

- The key is variable length, from 1 to 256 bytes.
- The internal state is a 256-byte permutation array `S`.
- Encryption and decryption are the same operation: `output = input XOR keystream`.
- No block modes (ECB/CBC), IV, or padding are needed, since the output length equals the input length.

---

## RC4 Scheme

```text
Key
 |
 v
KSA (Key-Scheduling Algorithm)
 |
 v
State S (256 bytes)
 |
 v
PRGA (Pseudo-Random Generation Algorithm)
 |
 v
Keystream K
 |
Plaintext XOR K -> Ciphertext
```

---

## Key-Scheduling Algorithm (KSA)

`S` is initialised to the identity permutation `[0, 1, ..., 255]`, then shuffled using the key.

```text
for i = 0 to 255:
    S[i] = i

j = 0
for i = 0 to 255:
    j = (j + S[i] + key[i mod keylength]) mod 256
    swap(S[i], S[j])
```

---

## Pseudo-Random Generation Algorithm (PRGA)

For each byte of data, one keystream byte is produced while the state keeps being shuffled.

```text
i = 0, j = 0
for each byte:
    i = (i + 1) mod 256
    j = (j + S[i]) mod 256
    swap(S[i], S[j])
    K = S[(S[i] + S[j]) mod 256]
```

---

## Encryption and Decryption

```text
Encryption: C = P XOR K

Decryption: P = C XOR K
```

Because XOR is its own inverse, the same keystream recovers the plaintext. The same key must never be reused for two different messages, otherwise `C1 XOR C2 = P1 XOR P2` leaks information.

---

## Usage

All files contain hex strings, same as the DES module.

```text
python RC4.py --enc <key> <input> <output>
python RC4.py --dec <key> <input> <output>
```

`--enc` and `--dec` perform the identical operation and are kept only for interface parity with the DES module.

Example (test vector, key = `Key`, plaintext = `Plaintext`):

```text
key.txt:    4B6579
input.txt:  506C61696E74657874
output.txt: BBF316E8D940AF0AD3
```

---

## Sources
https://www.geeksforgeeks.org/computer-networks/rc4-encryption-algorithm/

https://en.wikipedia.org/wiki/RC4
