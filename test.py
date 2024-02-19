#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')
privateKey = "MIIEowIBAAKCAQEA6HLk2H2nAAg96dmbdJ8MHvG6mvQUjvxP8MpJebQDK/urV6AXXvtH2cy5zhVpbnjMHjdhuxcTw9BYaiw55ZQrSsMRm3Xk2WgqpuqsbD8op8oOOd4fzqeRldEhgenyeaHhWj05Bb+quNCrLqt/cynShz8k8i2Vf7gSico39P+BH5AsdTbg0fUnmKnEbISRWYw36ot7G12GUXoRj98lbGgLGmIksbLV57nmsNR/I3WWvEoVfRXbGqDU4L1HKOVBcNVgQMYCZRnMWcs9Hn97TC73YOJ7i0R5iOl234YHW5ZblzVT3ynHD+BNGKsAd55//aPZ/gtml5I8cZ/J5JQNGUQrTwIDAQABAoIBAFGpi5xDCJiKTLYLLQIbnjaA1f36If7ZxXvilU2cYEDjeZ6fL5a+0M9DjUNJYnDdH1i+PCduRBNW7rjeMLjnBQ6O2XC0SmHWpqVdbJXa2n2YDsdlseb4F716azso5Xa12GXLfGz4mRG0vW738R6UYtIA7Qnn2c207U5bLK111fcwFAcsJ6LVA57fQtIl/Mie50xKOhRcbuFKZEsxF65aOl6wb8ZTYGxYoj7tnanLtGpeQjbHxjlQ5ONZSmx2fqDBaHf4upe6qlepucpGyMQng9FFctQ9DFol3z1DSPrOU47xGINGZdUkjocST2qI+Qg80Rfv5Wmj0JeR7xaEQQA2tIECgYEA9P7Lkz+/1rgTbrX4mg87D0wueSritjgPFK9x1NTW2WGVi35m/pGPGkKtZeg2mJ8CQwGVj1T76iOB4k6FVwoZA6ngmRyafh/DP8R0Ec9b971x2b8EtCoQqjS5U7068gDaIGa7zMwn5ztsURGJVqWaA8kWDJTL69bLMdJwVSM5mCsCgYEA8uPTkQHKJcguxwVCU6L1t+Hy6FZYQ5UiV4tUjflkRB/coGtM1WH8YciHNAMaXWbm52szedYcIXxRen42KdTbNsUjHVBxwxT7hTlN6c+Lkk8wir2pnZ5VOd0eHGx2pkg0sQUpYmLqWO0Rmp6P363mVKRQSeTI3p8Sbf3/4HkRo20CgYAwVvHN/P8aG7nh10/U/fpWO17UE40mDQuUtkVMjC5UN/fszST/R7MnqE5UVCwpkv48QFzFKiyGdzkScRHIKbrjySoCq+0jw5qfw2Bvfy2TRTLoltMTxVUCcGK8zhKKW3aue/bEIuggrM3jdQVXLlekNZH/K4DM6NWw3+fANLIRfwKBgCXvp4+yc9xK0+OJ0r41aaN6yvG26rpDhMWfoWk7Vom9YDw+BhYd48lyBIv/IBMOi2oBuFyDMImaXS+Anv0RnduEFuPxOJN7p307YgvuuqHzdGV3EhLoM++Btb5CwpVeGby8TaZsRKX3ARThRx9sjdkSgOfJsAX1Wm+LiHeK8VJRAoGBAOjBMZIn7GvLVaDGb1jk0TiDNJV0gcIygNLRsuA5fIsQqNvciTdOIuQRLC3fIo2phhzhsO4YhJyhGQ6RXWL8mjBmcGkRbbKhKz6dBIgMbPuE/Fj2WVST1envTMBNHQWCPtzMIn5AKAUoapgHyUt09/rlQDWzvolEqVocpps1psuh"
alipayPublicKey ="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgXvYmNiExfeBh0eXOwrB0pRdElrz1HIvtfJblQQIXCJekfe/IHkooHOsRpYm+nWN9yAadw43Z8ysq9gv2LUTvqzZNZeFzZSj1weA9heG+CMnpjGgM+iTeHMPZh8yGayP5H3rAL8IxLUoeOTZgxgPwh1i8pD9EkS8QDnr5K8aZoTVBSrB2nt72K7HWAeG3143KWRRD9hh3LYLAM1puynsLudWEGQYr7DUsio81mp6c5FilTz/JFZ8WemFhLVx58IhDlTLyY5umkTdLAGLSER8By3M+1so6ZQpBvCjskiuHJe3rCk8uXQGAsxYxZ7pAUZl/KSmiOeqv5SF2SmTYrGa6wIDAQAB"

if __name__ == '__main__':
    # 实例化客户端
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
    alipay_client_config.app_id = "9021000122694907"
    alipay_client_config.app_private_key = privateKey
    alipay_client_config.alipay_public_key = alipayPublicKey
    client = DefaultAlipayClient(alipay_client_config, logger)
    # 构造请求参数对象
    model = AlipayTradeCreateModel()
    model.out_trade_no = "20150320001001";
    model.total_amount = "88.88";
    model.subject = "Iphone6 16G";
    model.buyer_id = "2088722004564053";
    request = AlipayTradeCreateRequest(biz_model=model)
    # 执行API调用
    response_content = False
    try:
        response_content = client.page_execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        # # 解析响应结果
        print(response_content)
        # response = AlipayTradeCreateResponse()
        # response.parse_response_content(response_content)
        # # 响应成功的业务处理
        # if response.is_success():
        #     print(request)
        #     # 如果业务成功，可以通过response属性获取需要的值
        #     print("get response trade_no:" + response.trade_no)
        # # 响应失败的业务处理
        # else:
        #     # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
        #     print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
