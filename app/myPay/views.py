from rest_framework.views import APIView
from rest_framework.response import Response

from modelCore.models import MtPayInfo, Order
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
        customer_number = 1

        HashKey = '759ggsGGkvgL1dgs'
        HashIV = '3aHKRZzC4iJIhuX9'

        data = {
            'amount': amount,
            'customer_number': customer_number,
            'encrypt_type': encrypt_type,
            'merchant_id': merchant_id,
            'pay_content': pay_content,
            'payer_name': payer_name,
            'payment_method_id': payment_method_id,
            'return_url':return_url,
            'token': token,
        }

        data_str = f'HashKey={HashKey}&amount={amount}&customer_number={customer_number}&encrypt_type={encrypt_type}&merchant_id={merchant_id}&pay_content={pay_content}&payer_name={payer_name}&payment_method_id={payment_method_id}&return_url={return_url}&token={token}&HashIV={HashIV}'
        print(f'data str = {data_str}')

        url_encode_str = urllib.parse.quote(data_str, safe='')
        print(f'encode str = ${url_encode_str}')

        lower_url_encode_str = url_encode_str.lower()
        print(f'lower_url_encode_str = {lower_url_encode_str}')

        sign = sha256_hash(lower_url_encode_str)
        print(f'sign = {sign}')

        data['sign'] = sign

        resp = requests.post(url, json = data)
        return Response(json.loads(resp.text))

# http://localhost:8000/paymentApp/get_post_order
class GetPostOrderView(APIView):

     def get(self, request, format=None):
         
        token = 'F9E56960B9E7A0F9C768B053AB6DAA4E'
        merchant_id = 'wbl580'

        url = 'https://www.martinsss.com/api/order-encrypt'

        amount = 35
        encrypt_type  = 1
        pay_content = '測試商品'
        payer_name  = 'user0'
        payment_method_id = 1
        return_url = 'http://45.77.24.12/paymentApp/callback'
        customer_number = 1

        HashKey = '759ggsGGkvgL1dgs'
        HashIV = '3aHKRZzC4iJIhuX9'

        data = {
            'amount': amount,
            'customer_number': customer_number,
            'encrypt_type': encrypt_type,
            'merchant_id': merchant_id,
            'pay_content': pay_content,
            'payer_name': payer_name,
            'payment_method_id': payment_method_id,
            'return_url':return_url,
            'token': token,
        }

        data_str = f'HashKey={HashKey}&amount={amount}&customer_number={customer_number}&encrypt_type={encrypt_type}&merchant_id={merchant_id}&pay_content={pay_content}&payer_name={payer_name}&payment_method_id={payment_method_id}&return_url={return_url}&token={token}&HashIV={HashIV}'
        print(f'data str = {data_str}')

        url_encode_str = urllib.parse.quote(data_str, safe='')
        print(f'encode str = ${url_encode_str}')

        lower_url_encode_str = url_encode_str.lower()
        print(f'lower_url_encode_str = {lower_url_encode_str}')

        sign = sha256_hash(lower_url_encode_str)
        print(f'sign = {sign}')

        data['sign'] = sign

        resp = requests.post(url, json = data)
        resp_json = json.loads(resp.text)

        if resp_json['result']== 'success':

            mtPayInfo = MtPayInfo()
            mtPayInfo.order = Order.objects.get(id=1)
            mtPayInfo.status = 1
            mtPayInfo.amount = amount
            mtPayInfo.payment_number = resp_json['payment_number']
            mtPayInfo.number = resp_json['number']
            mtPayInfo.customer_number = resp_json['customer_number']
            mtPayInfo.save()

        return Response(resp_json)

#在這邊新增一個 GetUserPostOrderView 的 api
#帶入真實的資料
class GetUserPostOrderView(APIView):

     def get(self, request, format=None):
         
        token = 'F9E56960B9E7A0F9C768B053AB6DAA4E'
        merchant_id = 'wbl580'

        url = 'https://www.martinsss.com/api/order-encrypt'

        #帶入order資料
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)

        customer_number = 1 # 客戶訂單號
        # customer_number = order_id #這應該要再改
        
        payer_name  = 'user0'
        # payer_name = order.user.name
        
        amount = 35
        # amount = order.orderMoney

        encrypt_type  = 1
        pay_content = '測試商品'
        
        payment_method_id = 1
        return_url = 'http://45.77.24.12/paymentApp/callback'
        
        HashKey = '759ggsGGkvgL1dgs'
        HashIV = '3aHKRZzC4iJIhuX9'

        data = {
            'amount': amount,
            'customer_number': customer_number,
            'encrypt_type': encrypt_type,
            'merchant_id': merchant_id,
            'pay_content': pay_content,
            'payer_name': payer_name,
            'payment_method_id': payment_method_id,
            'return_url':return_url,
            'token': token,
        }

        

        data_str = f'HashKey={HashKey}&amount={amount}&customer_number={customer_number}&encrypt_type={encrypt_type}&merchant_id={merchant_id}&pay_content={pay_content}&payer_name={payer_name}&payment_method_id={payment_method_id}&return_url={return_url}&token={token}&HashIV={HashIV}'
        print(f'data str = {data_str}')

        url_encode_str = urllib.parse.quote(data_str, safe='')
        print(f'encode str = ${url_encode_str}')

        lower_url_encode_str = url_encode_str.lower()
        print(f'lower_url_encode_str = {lower_url_encode_str}')

        sign = sha256_hash(lower_url_encode_str)
        print(f'sign = {sign}')

        data['sign'] = sign

        resp = requests.post(url, json = data)
        resp_json = json.loads(resp.text)

        if resp_json['result']== 'success':

            mtPayInfo = MtPayInfo()
            mtPayInfo.order = Order.objects.get(id=1)
            mtPayInfo.status = 1 #1是已建立
            mtPayInfo.amount = amount
            mtPayInfo.payment_number = resp_json['payment_number']
            mtPayInfo.number = resp_json['number']
            mtPayInfo.customer_number = resp_json['customer_number']
            mtPayInfo.save()

        return Response(resp_json)

class CallBackView(APIView):


    # {
    #     "data":
    #     {
    #         "number": "MAT200408877CB",
    #         "amount": 20000,
    #         "status": 2,
    #         "pay_at": "2020-04-08 18:10:15",
    #         "pay_amount": 20000,
    #         "encrypt_type": 1,
    #         "return_url": "http://your.return.url",
    #         "payment_method_id": 1,
    #         "virtual_bank_id":0,
    #         "customer_number": "test123456",
    #         "sign": "0B4AC466CE1DF6ECFAB664DFDACD93B5BA7161787C150413B3B1402F3EEAB442"
    #     }
    # }

    def post(self, request, format=None):
        body = json.loads(request.body)
        logger.info(body)

        # data = body['data']
        # order_id = data['number']
        # amount = data['amount']

        return Response(body)

def sha256_hash(TradeInfo):
    hashs = hashlib.sha256(TradeInfo.encode("utf-8")).hexdigest()
    hashs = str.upper(hashs)
    return hashs