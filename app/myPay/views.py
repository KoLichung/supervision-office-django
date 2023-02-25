from rest_framework.views import APIView
from rest_framework.response import Response

import hashlib
import urllib.parse
import requests
import json
import logging

logger = logging.getLogger(__file__)

#http://localhost:8000/api/mypay/get_test
class GetTestView(APIView):

    def get(self, request, format=None):
        url = 'https://dev.martinsss.com/api/encrypt?token=F9E56960B9E7A0F9C768B053AB6DAA4E&merchant_id=wbl580&parameter=12345'
        resp = requests.get(url)
        return Response(json.loads(resp.text))

class GetPostTestView(APIView):

    def get(self, request, format=None):

        token = 'F9E56960B9E7A0F9C768B053AB6DAA4E'
        merchant_id = 'wbl580'
        parameter = '12345'

        url = 'https://dev.martinsss.com/api/encrypt'

        data = {
            'token': token,
            'merchant_id': merchant_id,
            'parameter': parameter,
        }

        resp = requests.post(url, json = data)
        return Response(json.loads(resp.text))
    
class GetPostTestOrderView(APIView):

    def get(self, request, format=None):

        token = 'F9E56960B9E7A0F9C768B053AB6DAA4E'
        merchant_id = 'wbl580'

        url = 'https://dev.martinsss.com/api/order-encrypt'

        amount = 200
        encrypt_type  = 1
        pay_content = '測試商品'
        payer_name  = 'user0'
        payment_method_id = 1
        return_url = 'http://45.77.24.12/paymentApp/callback'

        HashKey = '759ggsGGkvgL1dgs'
        HashIV = '3aHKRZzC4iJIhuX9'

        data = {
            'amount': amount,
            'encrypt_type': encrypt_type,
            'merchant_id': merchant_id,
            'pay_content': pay_content,
            'payer_name': payer_name,
            'payment_method_id': payment_method_id,
            'return_url':return_url,
            'token': token,
        }

        str = f'HashKey={HashKey}&amount={amount}&encrypt_type={encrypt_type}&merchant_id={merchant_id}&pay_content={pay_content}&payer_name={payer_name}&payment_method_id={payment_method_id}&return_url={return_url}&token=${token}&HashIV={HashIV}'
        
        url_encode_str = urllib.parse.quote(str)
        lower_url_encode_str = url_encode_str.lower()
        sign = sha256_hash(lower_url_encode_str)

        data['sign'] = sign

        resp = requests.post(url, json = data)
        return Response(json.loads(resp.text))

class CallBackView(APIView):

    def post(self, request, format=None):
        body = json.loads(request.body)
        logger.info(body)

def sha256_hash(TradeInfo):
    hashs = hashlib.sha256(TradeInfo.encode("utf-8")).hexdigest()
    hashs = str.upper(hashs)
    return hashs