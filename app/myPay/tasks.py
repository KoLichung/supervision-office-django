from modelCore.models import MtPayInfo, Order
import hashlib
import urllib.parse
import requests
import json
import logging

logger = logging.getLogger(__file__)

def post_order_to_mtPay(order_id):
    token = 'F9E56960B9E7A0F9C768B053AB6DAA4E'
    merchant_id = 'wbl580'

    url = 'https://www.martinsss.com/api/order-encrypt'

    #帶入order資料
    order = Order.objects.get(id=order_id)

    # customer_number = 1 # 客戶訂單號
    customer_number = int(order_id)

    # payer_name  = 'user0'
    payer_name = order.user.name
    
    # amount = 35
    amount = int(order.orderMoney)

    encrypt_type  = 1
    pay_content = '伍捌零商品'
    
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
    # print(f'data str = {data_str}')

    url_encode_str = urllib.parse.quote(data_str, safe='')
    # print(f'encode str = ${url_encode_str}')

    lower_url_encode_str = url_encode_str.lower()
    # print(f'lower_url_encode_str = {lower_url_encode_str}')

    sign = sha256_hash(lower_url_encode_str)
    # print(f'sign = {sign}')

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

        order.CVSInfoPaymentNo = mtPayInfo.payment_number
        order.CVSInfoExpireDate = mtPayInfo.query_limit_at
        order.save()

    print(resp_json)

    return resp_json

def sha256_hash(TradeInfo):
    hashs = hashlib.sha256(TradeInfo.encode("utf-8")).hexdigest()
    hashs = str.upper(hashs)
    return hashs