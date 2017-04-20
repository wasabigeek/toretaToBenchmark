import xmlrpc.client


class BMEApi(object):
    def __init__(self, username, password, ApiURL):
        BMEApi.isOk = True
        BMEApi.isLogin = True
        BMEApi.server = xmlrpc.client.Server(ApiURL)

        try:
            BMEApi.isLogin = True
            BMEApi.token = BMEApi.server.login(username, password)
            # print("Token : ", token)
        except xmlrpc.client.Fault as err:
            BMEApi.isLogin = False
            BMEApi.faultCode = err.faultCode
            BMEApi.faultString = err.faultString

    def getToken(self):
        return BMEApi.token

    def __getattr__(self, method_name):
            def get(self, *args, **kwargs):
                try:
                    result = getattr(BMEApi.server, method_name, None)(BMEApi.token, *args)
                    BMEApi.isOk = True
                    return result
                except xmlrpc.client.Fault as err:
                    BMEApi.isOk = False
                    BMEApi.faultCode = err.faultCode
                    BMEApi.faultString = err.faultString
                    return ""

            return get.__get__(self)
