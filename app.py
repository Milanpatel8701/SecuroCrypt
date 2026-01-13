# app.py
from flask import Flask, render_template, request, jsonify
from cipher import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    cipher_name = data.get('cipher', '')
    mode = data.get('mode', 'Encrypt')

    try:
        if cipher_name == 'Caesar Cipher':
            k = int(key)
            result = caesar_encrypt(text, k) if mode=='Encrypt' else caesar_decrypt(text, k)
        elif cipher_name == 'Rail Fence Cipher':
            k = int(key)
            result = rail_fence_encrypt(text, k) if mode=='Encrypt' else rail_fence_decrypt(text, k)
        elif cipher_name == 'Monoalphabetic Cipher':
            if mode=='Encrypt':
                result, _ = monoalphabetic_encrypt(text, key if key else None)
            else:
                result = monoalphabetic_decrypt(text, key)
        elif cipher_name == 'Polyalphabetic Cipher':
            key_shifts = [ord(c.upper())-65 for c in key]
            result = polyalphabetic_encrypt(text, key_shifts) if mode=='Encrypt' else polyalphabetic_decrypt(text, key_shifts)
        elif cipher_name == 'Vigenère Cipher':
            result = vigenere_encrypt(text, key) if mode=='Encrypt' else vigenere_decrypt(text, key)
        elif cipher_name == 'Playfair Cipher':
            result = playfair_encrypt(text, key) if mode=='Encrypt' else playfair_decrypt(text, key)
        elif cipher_name == 'Hill Cipher':
            numbers = [int(x) for x in key.split(',')]
            key_matrix = np.array(numbers).reshape(2,2)
            result = hill_encrypt(text,key_matrix) if mode=='Encrypt' else hill_decrypt(text,key_matrix)
        elif cipher_name == 'Transposition Cipher':
            k = int(key)
            result = transposition_encrypt(text,k) if mode=='Encrypt' else transposition_decrypt(text,k)
        elif cipher_name == 'Columnar Transposition Cipher':
            result = columnar_transposition_encrypt(text,key) if mode=='Encrypt' else columnar_transposition_decrypt(text,key)
        elif cipher_name == 'One-Time Pad':
            result = otp_encrypt(text,key) if mode=='Encrypt' else otp_decrypt(text,key)
        elif cipher_name == 'Homophonic Cipher':
            result = homophonic_encrypt(text) if mode=='Encrypt' else homophonic_decrypt(text)
        else:
            return jsonify({'error':'Cipher not recognized'})
        return jsonify({'result':result})
    except Exception as e:
        return jsonify({'error':str(e)})

app = Flask(__name__)

