
# ---------------
# CAESAR CIPHER 
# ---------------

def caesar_encrypt(text, key):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - 65 + key) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - 97 + key) % 26 + 97)
        else:
            result += char
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

# ------------------
# RAIL FENCE CIPHER 
# ------------------

def rail_fence_encrypt(text, rails):
    if rails <= 1:
        return text
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    result = ""
    for row in fence:
        result += "".join(row)
    return result

def rail_fence_decrypt(text, rails):
    if rails <= 1:
        return text
    fence = [[""] * len(text) for _ in range(rails)]
    rail = 0
    direction = 1
    for i in range(len(text)):
        fence[rail][i] = "*"
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    index = 0
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c] == "*" and index < len(text):
                fence[r][c] = text[index]
                index += 1
    result = ""
    rail = 0
    direction = 1
    for i in range(len(text)):
        result += fence[rail][i]
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return result

# --------------------------
# MONOALPHABETIC CIPHER
# --------------------------
import string
import random

def monoalphabetic_encrypt(text, key=None):
    letters = string.ascii_uppercase
    if key is None:
        key = list(letters)
        random.shuffle(key)
        key = ''.join(key)
    table = str.maketrans(letters, key)
    return text.upper().translate(table), key

def monoalphabetic_decrypt(text, key):
    letters = string.ascii_uppercase
    table = str.maketrans(key, letters)
    return text.upper().translate(table)

# --------------------------
# POLYALPHABETIC CIPHER (general, simple repeating shift)
# --------------------------
def polyalphabetic_encrypt(text, keys):
    result = ""
    keys_len = len(keys)
    for i, char in enumerate(text):
        if char.isalpha():
            base = 65 if char.isupper() else 97
            shift = keys[i % keys_len]
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def polyalphabetic_decrypt(text, keys):
    inverse_keys = [-k for k in keys]
    return polyalphabetic_encrypt(text, inverse_keys)

# --------------------------
# VIGENERE CIPHER
# --------------------------
def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    k = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[k % len(key)]) - 65
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
            k += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    k = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[k % len(key)]) - 65
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base - shift) % 26 + base)
            k += 1
        else:
            result += char
    return result

# --------------------------
# PLAYFAIR CIPHER
# --------------------------
def playfair_encrypt(text, key):
    # Prepare key matrix
    key = "".join(sorted(set(key.upper()), key=lambda x: key.index(x)))
    matrix = [c for c in key if c.isalpha()]
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for c in alphabet:
        if c not in matrix:
            matrix.append(c)
    matrix = [matrix[i*5:(i+1)*5] for i in range(5)]
    # Prepare text
    text = text.upper().replace("J","I")
    i = 0
    result = ""
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            b = 'X'
            i -= -1
        r1, c1, r2, c2 = None, None, None, None
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == a: r1, c1 = r, c
                if matrix[r][c] == b: r2, c2 = r, c
        if r1 == r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
        i += 2
    return result

def playfair_decrypt(text, key):
    key = "".join(sorted(set(key.upper()), key=lambda x: key.index(x)))
    matrix = [c for c in key if c.isalpha()]
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for c in alphabet:
        if c not in matrix:
            matrix.append(c)
    matrix = [matrix[i*5:(i+1)*5] for i in range(5)]
    i = 0
    result = ""
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        r1, c1, r2, c2 = None, None, None, None
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == a: r1, c1 = r, c
                if matrix[r][c] == b: r2, c2 = r, c
        if r1 == r2:
            result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
        i += 2
    return result

# --------------------------
# HILL CIPHER (2x2 for simplicity)
# --------------------------
import numpy as np

def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i])-65, ord(text[i+1])-65]
        enc_pair = np.dot(key_matrix, pair) % 26
        result += chr(enc_pair[0]+65) + chr(enc_pair[1]+65)
    return result

def hill_decrypt(text, key_matrix):
    det = int(np.linalg.det(key_matrix)) % 26
    inv_det = pow(det, -1, 26)
    inv_matrix = inv_det * np.round(np.linalg.inv(key_matrix) * det).astype(int) % 26
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i])-65, ord(text[i+1])-65]
        dec_pair = np.dot(inv_matrix, pair) % 26
        result += chr(int(dec_pair[0])+65) + chr(int(dec_pair[1])+65)
    return result

# --------------------------
# SIMPLE TRANSPOSITION CIPHER
# --------------------------
def transposition_encrypt(text, key):
    result = [''] * key
    for i, char in enumerate(text):
        result[i % key] += char
    return ''.join(result)

def transposition_decrypt(text, key):
    n_rows = len(text) // key
    extra = len(text) % key
    result = [''] * n_rows
    k = 0
    for i in range(key):
        col_len = n_rows + (1 if i < extra else 0)
        for j in range(col_len):
            result[j] += text[k]
            k += 1
    return ''.join(result)

# --------------------------
# COLUMNAR TRANSPOSITION CIPHER
# --------------------------
def columnar_transposition_encrypt(text, key):
    key_order = sorted(list(key))
    n_cols = len(key)
    n_rows = (len(text) + n_cols - 1) // n_cols
    grid = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    i = 0
    for r in range(n_rows):
        for c in range(n_cols):
            if i < len(text):
                grid[r][c] = text[i]
                i += 1
    ciphertext = ''
    for k in key_order:
        col_index = key.index(k)
        for r in range(n_rows):
            if grid[r][col_index] != '':
                ciphertext += grid[r][col_index]
    return ciphertext

def columnar_transposition_decrypt(text, key):
    key_order = sorted(list(key))
    n_cols = len(key)
    n_rows = (len(text) + n_cols - 1) // n_cols
    grid = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    col_lengths = [n_rows if i < len(text) % n_cols else n_rows-1 for i in range(n_cols)]
    k = 0
    for ki in key_order:
        col_index = key.index(ki)
        for r in range(col_lengths[col_index]):
            grid[r][col_index] = text[k]
            k += 1
    plaintext = ''
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] != '':
                plaintext += grid[r][c]
    return plaintext

# --------------------------
# ONE-TIME PAD
# --------------------------
def otp_encrypt(text, key):
    result = ""
    for i, char in enumerate(text):
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char)-base + ord(key[i % len(key)].upper())-65)%26 + base)
        else:
            result += char
    return result

def otp_decrypt(ciphertext, key):
    result = ""
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char)-base - (ord(key[i % len(key)].upper())-65))%26 + base)
        else:
            result += char
    return result

# --------------------------
# HOMOPHONIC CIPHER (simple letter->number map)
# --------------------------
homophonic_map = {
    'A':['11','12'], 'B':['21','22'], 'C':['31','32'], 'D':['41','42'], 'E':['51','52'],
    'F':['13','14'], 'G':['23','24'], 'H':['33','34'], 'I':['43','44'], 'J':['53','54'],
    'K':['15','16'], 'L':['25','26'], 'M':['35','36'], 'N':['45','46'], 'O':['55','56'],
    'P':['17','18'], 'Q':['27','28'], 'R':['37','38'], 'S':['47','48'], 'T':['57','58'],
    'U':['19','20'], 'V':['29','30'], 'W':['39','40'], 'X':['49','50'], 'Y':['59','60'], 'Z':['61','62']
}

def homophonic_encrypt(text):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += random.choice(homophonic_map[char])
        else:
            result += char
    return result

def homophonic_decrypt(ciphertext):
    # For simplicity, decryption is not implemented (requires mapping of numbers to letters)
    return "Decryption not implemented for Homophonic Cipher"
