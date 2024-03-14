import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse

from sever import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')
if __name__ == '__main__':
    # 实例化客户端
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
    alipay_client_config.app_id = settings.APP_ID
    alipay_client_config.app_private_key = settings.PRIVATEKEY
    alipay_client_config.alipay_public_key = settings.ALIPAYPUBLICKEY
    client = DefaultAlipayClient(alipay_client_config, logger)
    # 构造请求参数对象
    model = AlipayTradeCreateModel()
    model.out_trade_no = "20150320010101001";
    model.total_amount = "88.88";
    model.subject = "Iphone6 16G";
    model.buyer_id = "2088722004564053";
    request = AlipayTradeCreateRequest(biz_model=model)
    # 执行API调用
    response_content = False
    try:
        response_content = client.execute(request)

    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        # 解析响应结果
        response = AlipayTradeCreateResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            print(response_content)
            print("get response trade_no:" + response.trade_no)
            print("get response trade_no:" + response.out_trade_no)
            print("get response trade_no:" + response.msg)
            print("get response trade_no:" + response.body)
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)