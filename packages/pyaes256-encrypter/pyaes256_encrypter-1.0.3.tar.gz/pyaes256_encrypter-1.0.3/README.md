# pyaes256_encrypter
A package to simplify the use of AES-256 encryption with random initialization vector.

## Install
```
pip install pyaes256-encrypter
```

## Usage
~~~python
  from aes256_encrypter import encode_text,decode_text
  
  text = 'hello world'                        # text to be encrypted
  key = 'key'                                 # encryption key
  
  encoded = encode_text(text,key)             # 'Dx3dCTUSXzzM8wn1L/+NHVbyaDxZFpdqe+SN2NVZgfE='
  decoded = decode_text(encoded,key)          # 'hello world'
  
~~~