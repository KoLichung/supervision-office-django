from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
import urllib.parse
import base64

class AESCipher(object):

    def __init__(self):
        # self.key = 'VBLWL1eyv1H3dyeU'.encode('utf8')
        # self.iv = '2XGjZEOT3m9wZfBP'.encode('utf8')

        # 以下為測試用 # "MerchantID": "3002607"
        self.key = 'pwFHCqoQZGmho4w6'.encode('utf8')
        self.iv = 'EkRm7iFT261dpevs'.encode('utf8')
        self.mode = AES.MODE_CBC

    # command line test
    # from payECPay.aesCipher import AESCipher
    # cipher = AESCipher()
    # cipher.test()

    def test(self):
        # data = '{"Name":"Test","ID":"A123456789"}'
        data1 = {
            "Name":"Test",
            "ID":"A123456789"
        }
        # print(str(data1).replace(" ",'').replace("'",'"'))
        # encode_text = urllib.parse.quote(data)
        encode_text = urllib.parse.quote(str(data1).replace(" ",'').replace("'",'"'))
        print(encode_text)
        
        cipher = AESCipher()
        encrypt_text = cipher.encrypt(encode_text)
        print(encrypt_text)

        print()
        print()

        decrypt_text = cipher.decrypt(encrypt_text)
        print(decrypt_text)

        the_data = urllib.parse.unquote(decrypt_text)
        print(the_data)

    def encrypt(self, text):
        cipher = AES.new(self.key, self.mode, self.iv)
        text= self.pkcs7_padding(text)
        ciphertext = base64.b64encode(cipher.encrypt(text)).decode('utf8')
        return ciphertext

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    
    def decrypt(self, text):
        cipher = AES.new(self.key, self.mode, self.iv)

        encode_text = text.encode('utf8')
        base64DecodeText = base64.b64decode(encode_text)
        text = cipher.decrypt(base64DecodeText)

        decrypt_text = self.pkcs7_unpadding(text).decode('utf8')

        return decrypt_text
        # return plain_text.rstrip('\0')
        # return bytes.decode(plain_text).rstrip("\x01").\
        #     rstrip("\x02").rstrip("\x03").rstrip("\x04").rstrip("\x05").\
        #     rstrip("\x06").rstrip("\x07").rstrip("\x08").rstrip("\x09").\
        #     rstrip("\x0a").rstrip("\x0b").rstrip("\x0c").rstrip("\x0d").\
        #     rstrip("\x0e").rstrip("\x0f").rstrip("\x10")

    @staticmethod
    def pkcs7_unpadding(padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)

        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise Exception('无效的加密信息!')
        else:
            return uppadded_data