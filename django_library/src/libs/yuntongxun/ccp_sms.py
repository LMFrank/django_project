# -*- coding:utf-8 -*-

# import ssl
# ssl._create_default_https_context =ssl._create_stdlib_context # 解决Mac开发环境下，网络错误的问题


from .CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = ''

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = ''

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = ''

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

# 发送模板短信
# def send_template_sms(to, datas, tempId):
#     """
#     云通讯官方提供的发送短信代码实例
#     :param to: 手机号码
#     :param datas: 内容数据 格式为列表 例如：['123456', '5']，如不需替换请填 ''
#     :param tempId: 模板Id
#     :return: 成功、失败
#     """
#     # 初始化REST SDK
#     rest = REST(_serverIP, _serverPort, _softVersion)
#     rest.setAccount(_accountSid, _accountToken)
#     rest.setAppId(_appId)
#
#     # 调用发送短信的接口函数
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     print(result)


class CCP(object):
    """单例类：初始化并提供单例的"""

    def __new__(cls, *args, **kwargs):
        """初始化并提供单例的"""
        # 判断单例是否存在：相当于判断有没有女朋友、男朋友
        # hasattr('要判断的类对象', '单例属性名')
        if not hasattr(CCP, '_instance'):
            # 如果没有单例，就new一个：相当于如果没有女朋友、男朋友，就找一个
            # cls : 表示当前的类对象CCP，我们将创建出来的对象绑定到CCP
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)

            # 初始化REST SDK:保证rest对象跟单例是同生共死的
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)

        # 如果有单例就返回：如果有女朋友、男朋友，就带出去玩儿
        return cls._instance

    def send_template_sms(self, to, datas, tempId):
        """
        发送短信验证码的单例方法
        :param self: 表示的就是调用这个方法的单例（self == _instance）
        :param to: 手机号
        :param datas: 内容数据 ['验证码', '过期时间']
        :param tempId: 模板ID
        :return: 成功：0 或者 失败：-1
        """
        # 调用发送短信的接口函数
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # 模拟网络延迟：没有实际的意义
        import time
        time.sleep(5)

        print(result)
        if result.get('statusCode') == '000000':
            return 0
        else:
            return -1


if __name__ == '__main__':
    # 注意：测试的短信模板编号为1
    # 必须先使用CCP()初始化单例，才能够调用发送短信验证码的单例方法
    CCP().send_template_sms('17012345678', ['111111', 5], 1)
