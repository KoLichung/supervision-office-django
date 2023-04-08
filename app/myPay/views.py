from rest_framework.views import APIView
from rest_framework.response import Response

from modelCore.models import MtPayInfo, Order, OrderState
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
        customer_number = 71

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
            mtPayInfo.order = Order.objects.get(id=10)
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

        # customer_number = 1 # 客戶訂單號
        customer_number = int(order_id)

        payer_name  = 'user0'
        # payer_name = order.user.name #flutter的Order只有 user id 沒有 user name
        
        # amount = 35
        amount = int(order.orderMoney)

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
            mtPayInfo.order = Order.objects.get(id=int(order_id))
            mtPayInfo.status = 1 #1是已建立
            mtPayInfo.amount = amount
            mtPayInfo.payment_number = resp_json['payment_number']
            mtPayInfo.number = resp_json['number']
            mtPayInfo.customer_number = resp_json['customer_number']
            mtPayInfo.query_limit_at = resp_json['query_limit_at'] #新增了這行
            mtPayInfo.save()

        return Response(resp_json)

class CallBackView(APIView):


    # {
    #     "data": {
    #         "number": "MAT200408877CB",
    #         "amount": 20000,
    #         "status": 2,
    #         "pay_at": "2020-04-08 18:10:15",
    #         "pay_amount": 20000,
    #         "encrypt_type": 1,
    #         "return_url": "http://your.return.url",
    #         "payment_method_id": 1,
    #         "virtual_bank_id": 0,
    #         "customer_number": "test123456",
    #         "payment_records": "%5B%7B%22tx_number%22%3A%22tx888888888%22%2C%22out_bank_code%22%3A%22123%22%2C%22out_bank_account%22%3A%22123456789%22%2C%22pay_amount%22%3A20000%2C%22pay_at%22%3A%222020-04-08+18%3A10%3A15%22%7D%5D",
    #         "sign": "C8F24BE27B01DC553F8156A53708522F270D56475861FE82F25BE60373388274"
    #     }
    # }

    def post(self, request, format=None):
        body = json.loads(request.body)
        logger.info(body)

        data = body['data']
        order_id = data['customer_number']
        status = data['status']

        try:
            order = Order.objects.get(id=order_id)
            mtPayInfo = MtPayInfo.objects.get(order=order)
            mtPayInfo.status = status

            if data['pay_at'] != None:
                mtPayInfo.pay_at = data['pay_at']

            if data['payment_records'] != None:
                mtPayInfo.payment_records = data['payment_records']

            if data['pay_amount'] != None:
                mtPayInfo.pay_amount = data['pay_amount']

            if data['encrypt_type'] != None:
                mtPayInfo.encrypt_type = data['encrypt_type']
                
            if data['sign'] != None:
                mtPayInfo.pay_amount = data['sign']

            if mtPayInfo.status == 2:
                order.state = OrderState.objects.get(name='已完成')
                order.save()

            mtPayInfo.save()

        except Exception as e:
            logger.error(e)

        return Response(body)

def sha256_hash(TradeInfo):
    hashs = hashlib.sha256(TradeInfo.encode("utf-8")).hexdigest()
    hashs = str.upper(hashs)
    return hashs