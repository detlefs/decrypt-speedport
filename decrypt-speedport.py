#!/usr/bin/env python3
# Speedport Smart 4 - Status.json Entschlüsseler (korrekt: AES-CCM)

from Crypto.Cipher import AES
import json, sys

KEY_HEX = "cdc0cac1280b516e674f0057e4929bca84447cca8425007e33a88a5cf598a190"

def decode(data: str) -> dict:
    key = bytes.fromhex(KEY_HEX)
    nonce = key[:8]
    
    hex_clean = data.strip().replace('\n','').replace('\r','').replace(' ','')
    if len(hex_clean) % 2:
        hex_clean = hex_clean[:-1]
    
    ciphertext_tag = bytes.fromhex(hex_clean)
    ciphertext = ciphertext_tag[:-16]
    tag = ciphertext_tag[-16:]
    
    cipher = AES.new(key, AES.MODE_CCM, nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    return json.loads(decrypted.decode('utf-8'))

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        raw = f.read()
    result = decode(raw)
    print(json.dumps(result, indent=2, ensure_ascii=False))