exception_info_dict = {
    # 执行命令异常 30000

    # 代码异常   20000

    # 初始化异常 10000
    'init_error': 10001
}


class HostClientException(Exception):
    def __init__(self, message=None, code=None):
        if message is None:
            message = 'Unknown Error'
        if code is None:
            code = 00000
        self.message = message
        self.code = code


class InitHostException(HostClientException):
    def __init__(self):
        super().__init__('Init Error', 10001)


class ExecuteCommandException(HostClientException):
    def __init__(self, error):
        super().__init__(f'Execute Command Error:{error}', 30001)


class SFTPException(HostClientException):
    pass
