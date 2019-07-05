from random import randint

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from Ecommerce.settings import SMSCONFIG


def send_sms(phone, templateParam, **kwargs):

    client = AcsClient(kwargs['ACCESS_KEY_ID'], kwargs['ACCESS_KEY_SECRET'], 'default')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', kwargs['SignName'])
    request.add_query_param('TemplateCode', kwargs['TemplateCode'])
    request.add_query_param('TemplateParam', templateParam)

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


if __name__ == "__main__":
    send_sms('phone', {'code': 'num'}, **SMSCONFIG)

