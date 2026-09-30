# ============================================================
# DES - MANUAL IMPLEMENTATION
# ============================================================

BLOCK_SIZE = 8


# ============================================================
# DES TABLES
# ============================================================

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFTS = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]


# ============================================================
# S-BOX
# ============================================================

S_BOX = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]


# ============================================================
# BASIC FUNCTIONS
# ============================================================

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)


def xor_bits(a, b):
    return ''.join(
        '0' if x == y else '1'
        for x, y in zip(a, b)
    )


def left_shift(bits, n):
    return bits[n:] + bits[:n]


# ============================================================
# KEY SCHEDULE
# ============================================================

def generate_subkeys(key_64):
    # PC-1: 64 -> 56
    key_56 = permute(key_64, PC1)

    C = key_56[:28]
    D = key_56[28:]

    subkeys = []

    for shift in SHIFTS:
        C = left_shift(C, shift)
        D = left_shift(D, shift)

        # PC-2: 56 -> 48
        subkey = permute(C + D, PC2)

        subkeys.append(subkey)

    return subkeys


# ============================================================
# S-BOX
# ============================================================

def sbox_substitution(bits_48):
    result = ''

    for i in range(8):
        block = bits_48[i * 6:(i + 1) * 6]

        row = int(
            block[0] + block[5],
            2
        )

        column = int(
            block[1:5],
            2
        )

        value = S_BOX[i][row][column]

        result += format(value, '04b')

    return result


# ============================================================
# FEISTEL FUNCTION
# ============================================================

def feistel(R, subkey):

    # 32 -> 48
    expanded = permute(R, E)

    # XOR
    xored = xor_bits(
        expanded,
        subkey
    )

    # 48 -> 32
    substituted = sbox_substitution(
        xored
    )

    # Permutation P
    return permute(
        substituted,
        P
    )


# ============================================================
# DES ENCRYPT
# ============================================================

def des_encrypt(block_64, key_64):

    if len(block_64) != 64:
        raise ValueError(
            "Block plaintext harus 64 bit."
        )

    if len(key_64) != 64:
        raise ValueError(
            "Key harus 64 bit."
        )

    # Generate K1-K16
    subkeys = generate_subkeys(
        key_64
    )

    # Initial Permutation
    block = permute(
        block_64,
        IP
    )

    # Split
    L = block[:32]
    R = block[32:]

    # 16 rounds
    for i in range(16):

        new_L = R

        new_R = xor_bits(
            L,
            feistel(
                R,
                subkeys[i]
            )
        )

        L = new_L
        R = new_R

    # Swap + Final Permutation
    return permute(
        R + L,
        FP
    )


# ============================================================
# DES DECRYPT
# ============================================================

def des_decrypt(block_64, key_64):

    if len(block_64) != 64:
        raise ValueError(
            "Block ciphertext harus 64 bit."
        )

    if len(key_64) != 64:
        raise ValueError(
            "Key harus 64 bit."
        )

    # Generate K1-K16
    subkeys = generate_subkeys(
        key_64
    )

    # Decryption menggunakan:
    # K16 -> K15 -> ... -> K1
    subkeys.reverse()

    # Initial Permutation
    block = permute(
        block_64,
        IP
    )

    # Split
    L = block[:32]
    R = block[32:]

    # 16 rounds
    for i in range(16):

        new_L = R

        new_R = xor_bits(
            L,
            feistel(
                R,
                subkeys[i]
            )
        )

        L = new_L
        R = new_R

    # Swap + Final Permutation
    return permute(
        R + L,
        FP
    )


# ============================================================
# BYTE <-> BIT
# ============================================================

def bytes_to_bits(data):
    if isinstance(data, str):
        data = data.encode("ascii")

    return ''.join(
        format(byte, '08b')
        for byte in data
    )


def bits_to_bytes(bits):
    result = bytearray()

    for i in range(0, len(bits), 8):
        result.append(
            int(bits[i:i + 8], 2)
        )

    return bytes(result)


# ============================================================
# KEY VALIDATION
# ============================================================

def validate_key(key):

    if isinstance(key, str):
        key = key.encode("ascii")

    if not isinstance(key, (bytes, bytearray)):
        raise TypeError(
            "Key harus berupa string atau bytes."
        )

    if len(key) != 8:
        raise ValueError(
            "Key harus tepat 8 karakter."
        )

    return bytes(key)


# ============================================================
# PADDING
# ============================================================

def pad(data):

    padding_length = BLOCK_SIZE - (
        len(data) % BLOCK_SIZE
    )

    return (
        data +
        bytes([padding_length]) *
        padding_length
    )


def unpad(data):

    padding_length = data[-1]

    if (
        padding_length < 1
        or padding_length > BLOCK_SIZE
    ):
        raise ValueError(
            "Padding tidak valid."
        )

    if (
        data[-padding_length:]
        != bytes([padding_length]) * padding_length
    ):
        raise ValueError(
            "Padding tidak valid."
        )

    return data[:-padding_length]


# ============================================================
# ENCRYPT BLOCK
# ============================================================

def encrypt_block(block, key):

    if len(block) != BLOCK_SIZE:
        raise ValueError(
            "Block DES harus 8 byte."
        )

    key = validate_key(key)

    block_bits = bytes_to_bits(block)
    key_bits = bytes_to_bits(key)

    encrypted_bits = des_encrypt(
        block_bits,
        key_bits
    )

    return bits_to_bytes(
        encrypted_bits
    )


# ============================================================
# DECRYPT BLOCK
# ============================================================

def decrypt_block(block, key):

    if len(block) != BLOCK_SIZE:
        raise ValueError(
            "Block DES harus 8 byte."
        )

    key = validate_key(key)

    block_bits = bytes_to_bits(block)
    key_bits = bytes_to_bits(key)

    decrypted_bits = des_decrypt(
        block_bits,
        key_bits
    )

    return bits_to_bytes(
        decrypted_bits
    )


# ============================================================
# ENCRYPT TEXT
# ============================================================

def encrypt_text(plaintext, key):

    key = validate_key(key)

    data = plaintext.encode("utf-8")

    data = pad(data)

    ciphertext = bytearray()

    for i in range(
        0,
        len(data),
        BLOCK_SIZE
    ):

        block = data[
            i:i + BLOCK_SIZE
        ]

        encrypted_block = encrypt_block(
            block,
            key
        )

        ciphertext.extend(
            encrypted_block
        )

    return ciphertext.hex().upper()


# ============================================================
# DECRYPT TEXT
# ============================================================

def decrypt_text(ciphertext_hex, key):

    key = validate_key(key)

    try:
        ciphertext = bytes.fromhex(
            ciphertext_hex
        )

    except ValueError:
        raise ValueError(
            "Ciphertext harus berupa HEX."
        )

    if not ciphertext:
        raise ValueError(
            "Ciphertext kosong."
        )

    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError(
            "Ciphertext harus kelipatan 8 byte."
        )

    plaintext = bytearray()

    for i in range(
        0,
        len(ciphertext),
        BLOCK_SIZE
    ):

        block = ciphertext[
            i:i + BLOCK_SIZE
        ]

        decrypted_block = decrypt_block(
            block,
            key
        )

        plaintext.extend(
            decrypted_block
        )

    plaintext = unpad(
        bytes(plaintext)
    )

    return plaintext.decode("utf-8")


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    plaintext = "HALO1234"
    key = "KUNCIDES"

    print("=" * 40)
    print("DES SELF TEST")
    print("=" * 40)

    print("Plaintext :", plaintext)
    print("Key       :", key)

    ciphertext = encrypt_text(
        plaintext,
        key
    )

    print("Ciphertext:", ciphertext)

    decrypted = decrypt_text(
        ciphertext,
        key
    )

    print("Decrypted :", decrypted)

    if decrypted == plaintext:
        print("TEST      : SUCCESS")
    else:
        print("TEST      : FAILED")