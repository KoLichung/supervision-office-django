from rest_framework.views import APIView
from rest_framework.response import Response
from .aesCipher import AESCipher
from datetime import datetime, timedelta
from random import randint

import requests
import json
import time
import urllib.parse
import logging

from modelCore.models import PayInfo, Order

logger = logging.getLogger(__file__)

def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

class GetTokenView(APIView):

    def get(self, request, format=None):

        order_id = self.request.query_params.get('order_id')
        merchantTradeNo = f"A{order_id}{random_with_N_digits(6)}"

        order = Order.objects.get(id=order_id)

        post_url = 'https://ecpg-stage.ecpay.com.tw/Merchant/GetTokenbyTrade'
        # post_url = 'https://ecpg.ecpay.com.tw/Merchant/GetTokenbyTrade'
        timeStamp = int( time.time() )
        
        # 測試用
        merchandID= "3002607"
        # 正式用
        # merchandID= "1332298"

        data = {
                "MerchantID": merchandID,
                "RememberCard": 0,
                "PaymentUIType": 2,
                "ChoosePaymentList": "1,3",
                "OrderInfo": {
                    "MerchantTradeNo": merchantTradeNo,
                    "MerchantTradeDate": (datetime.now()+timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S"),
                    "TotalAmount": f"{order.orderMoney}",
                    "ReturnURL": "https://336d-125-230-206-99.jp.ngrok.io/api/ecpay/post_callback",
                    "TradeDesc": "監所購物",
                    "ItemName": f"訂單編號{order.id}"
                },
                "CardInfo": {
                    "OrderResultURL": "https://www.ecpay.com.tw/",
                    "CreditInstallment": "3,6,9,12"
                },
                "ATMInfo": {
                    "ExpireDate": 3
                },
                "ConsumerInfo": {
                    "MerchantMemberID": f"{order.user.id}",
                    "Email": "customer@email.com",
                    "Phone": f"{order.user.phone}",
                    "Name": f"{order.user.name}",
                    "CountryCode": "158"
                },
                "CustomField": f"{order_id}",
        }
        
        print(str(data).replace(": ",':').replace(", ",',').replace("'",'"'))
        #url encode
        encode_text = urllib.parse.quote(str(data).replace(": ",':').replace(", ",',').replace("'",'"'))

        cipher = AESCipher()
        encrypt_text = cipher.encrypt(encode_text)

        postData = {
            "MerchantID": merchandID,
            "RqHeader": {
                "Timestamp": str(timeStamp),
                "Revision": "1.3.22"
            },
            "Data": encrypt_text
        }

        resp = requests.post(post_url, json = postData)

        respData = json.loads(resp.text)['Data']
        decrypt_text = cipher.decrypt(respData)
        the_data = urllib.parse.unquote(decrypt_text)

        return Response(json.loads(the_data))

class PaymentResultCallback(APIView):

    def post(self, request, format=None):
        # body_unicode = request.body.decode('utf-8')
        body = json.loads(request.body)
        # print(body)
        
        cipher = AESCipher()
        data = body['Data']
        decrypt_text = cipher.decrypt(data)
        the_data = urllib.parse.unquote(decrypt_text)

        data_json = json.loads(the_data)
        
        print(data_json)
        logger.info(body)
        logger.info(data_json)

        if(PayInfo.objects.filter(OrderInfoMerchantTradeNo=data_json['OrderInfo']['MerchantTradeNo']).count()==0 ):
            payInfo = PayInfo()
            payInfo.MerchantID = data_json['MerchantID']

            if( 'OrderInfo' in data_json):
                payInfo.OrderInfoMerchantTradeNo = data_json['OrderInfo']['MerchantTradeNo']
                payInfo.OrderInfoTradeDate = datetime.strptime(data_json['OrderInfo']['TradeDate'], "%Y/%m/%d %H:%M:%S")  
                payInfo.OrderInfoTradeNo = data_json['OrderInfo']['TradeNo']
                payInfo.OrderInfoTradeAmt = data_json['OrderInfo']['TradeAmt']
                payInfo.OrderInfoPaymentType = data_json['OrderInfo']['PaymentType']
                payInfo.OrderInfoChargeFee = data_json['OrderInfo']['ChargeFee']
                try:
                    payInfo.OrderInfoTradeStatus = data_json['OrderInfo']['TradeStatus']
                except:
                    logger.info("no trade status")
            

            if('CardInfo' in data_json and data_json['CardInfo']!= None):
                payInfo.PaymentType = "信用卡"
                payInfo.CardInfoAuthCode = data_json['CardInfo']['AuthCode']
                payInfo.CardInfoGwsr = data_json['CardInfo']['Gwsr']
                payInfo.CardInfoProcessDate = datetime.strptime(data_json['CardInfo']['ProcessDate'], "%Y/%m/%d %H:%M:%S")  
                payInfo.CardInfoAmount = data_json['CardInfo']['Amount']
                payInfo.CardInfoCard6No = data_json['CardInfo']['Card6No']
                payInfo.CardInfoCard4No = data_json['CardInfo']['Card4No']
            
            if('ATMInfo' in data_json and data_json['ATMInfo']!= None):
                print("atm info")
                # 3碼
                payInfo.ATMInfoBankCode = data_json['ATMInfo']['ATMAccBank']
                # 後 5 碼
                payInfo.ATMInfovAccount = data_json['ATMInfo']['ATMAccNo']
            else:
                print("no atm info")

            if('CustomField' in data_json and data_json['CustomField']!= None):
                try:
                    order = Order.objects.get(id= int(data_json['CustomField']))
                    order.state = 'ownerWillContact'
                    order.save()
                    payInfo.order = order
                    payInfo.save()
                except:
                    print("can't find order custom field error")
            else:
                order = Order.objects.get(id=1)
                order.state = 'ownerWillContact'
                order.save()
                payInfo.order = Order.objects.get(id=1)
                payInfo.save()
            
            
        # print(the_data)

        # content = body['content']
        # print(content)

        return Response("1|OK")

    