from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeRefundModel import AlipayTradeRefundModel
from alipay.aop.api.util.SignatureUtils import verify_with_rsa

from sever import settings


def alipayConfig():
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = settings.ALIPAYSEVER
    alipay_client_config.app_id = settings.APP_ID
    alipay_client_config.app_private_key = settings.PRIVATEKEY
    alipay_client_config.alipay_public_key = settings.ALIPAYPUBLICKEY
    return alipay_client_config


def alipayModel(orderNo: int, totalAmount: str, subject: str):
    '''
    支付参数
    :param orderNo: 订单号
    :param totalAmount: 金额，单位为元，精确到小数点后两位
    :param subject: 订单标题
    :return:
    '''
    model = AlipayTradePagePayModel()
    model.out_trade_no = orderNo  # 商户订单号，商户网站订单系统中唯一订单号，必填
    model.total_amount = totalAmount  # 订单总金额，单位为元，精确到小数点后两位
    model.subject = subject  # 订单标题
    # model.qr_pay_mode = "0"  # 扫码支付请求必须
    model.product_code = "FAST_INSTANT_TRADE_PAY"  # 电脑网站支付请求必须
    model.timeout_express = "5m"  # 订单过期时间
    return model

def refundModel(orderNo: int, refundAmount: str, refundReason: str):
    '''
    退款参数
    :param orderNo: 订单号
    :param refundAmount: 退款金额，单位为元，精确到小数点后两位
    :param refundReason: 退款原因
    :return:
    '''
    model = AlipayTradeRefundModel()
    model.out_trade_no = orderNo  # 商户订单号，商户网站订单系统中唯一订单号，必填
    model.refund_amount = refundAmount  # 退款金额，单位为元，精确到小数点后两位
    model.refund_reason = refundReason  # 退款原因
    return model


def check_pay(params):  # 定义检查支付结果的函数
    sign = params.pop('sign', None)  # 取出签名
    params.pop('sign_type')  # 取出签名类型
    params = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
    message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()  # 将列表转为二进制参数字符串
    try:
        status = verify_with_rsa(settings.ALIPAYPUBLICKEY.encode('utf-8').decode('utf-8'), message,
                                 sign)  # 验证签名并获取结果
        return status  # 返回验证结果
    except:  # 如果验证失败，返回假值。
        return False


def add_day(date_string, days):
    from datetime import datetime, timedelta
    # 将字符串转换为datetime对象
    date_time = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    # 加一天
    new_date_time = date_time + timedelta(days=days)
    # 将结果转换回字符串并返回
    return new_date_time.strftime('%Y-%m-%d %H:%M:%S')


