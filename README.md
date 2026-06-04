# decrypt-speedport

A Python utility to decrypt the encrypted `status.json` response from the **Telekom Speedport Smart 4** router.

## Background

The Speedport Smart 4 exposes its status data via an internal API endpoint (e.g. `http://speedport.ip/api/status`). The response is AES-CCM encrypted. This tool decrypts that payload using the router's known fixed key and outputs the plain JSON.

**Note:** The router's known fixed key can be changed at any time with a firmware update. In that case the script will stop working.

## Requirements

- Python 3
- [pycryptodome](https://pycryptodome.readthedocs.io/)

```bash
pip install pycryptodome
```

## Usage

```bash
curl -s http://speedport.ip/data/Status.json -o status.hex
python decrypt-speedport.py status.hex > status.json
```

The decrypted JSON is directed to status.json.

## How It Works

The encrypted payload is treated as `ciphertext || tag` (the last 16 bytes are the AES-CCM authentication tag). Decryption uses:

- **Algorithm**: AES-CCM
- **Key**: 256-bit fixed key hardcoded in the script
- **Nonce**: first 8 bytes of the key

## Notes

- The hardcoded key is a known constant for the Speedport Smart 4 firmware.
- If the tag verification fails, `pycryptodome` will raise a `ValueError` — this indicates either a wrong key or corrupted/modified data.
