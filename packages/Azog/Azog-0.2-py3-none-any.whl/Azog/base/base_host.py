import paramiko

from Azog.base.exception import ExecuteCommandException, InitHostException, SFTPException


class BaseHost:
    def __init__(self, host_connect_info=None, client=None):
        self.connect_address = None
        self.connect_port = None
        self.connect_name = None
        self.connect_password = None
        if host_connect_info and not client:
            self._init_ssh_client(host_connect_info)
        # 如果只传host信息就初始化  只传client 就是初始化工具类
        if client and not host_connect_info:
            self._client = client

    def _init_ssh_client(self, host_connect_info):
        self.connect_address = host_connect_info.get('Address', None)
        self.connect_port = host_connect_info.get('Port', None)
        self.connect_name = host_connect_info.get('User', None)
        self.connect_password = host_connect_info.get('Password', None)
        if not all([self.connect_port, self.connect_address, self.connect_name, self.connect_password]):
            raise InitHostException()

        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(self.connect_address, self.connect_port, self.connect_name, self.connect_password)

    def execute(self, command: str) -> str:
        stdin, stdout, stderr = self._client.exec_command(command)
        rsp = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            raise ExecuteCommandException(error)
        return rsp.strip()

    def _init_sftp_transfer_file(self):
        try:
            t = paramiko.Transport((self.connect_address, self.connect_port))
            t.connect(username=self.connect_name, password=self.connect_password)
            sftp = paramiko.SFTPClient.from_transport(t)
            return sftp
        except Exception as e:
            print(e)

    def sftp_get(self, server_path, local_path):
        sftp = self._init_sftp_transfer_file()

        try:
            sftp.get(server_path, local_path)
        except SFTPException as e:
            print(e)
        finally:
            sftp.close()

    def sftp_put(self, local_path, server_path):
        sftp = self._init_sftp_transfer_file()

        try:
            sftp.put(local_path, server_path)
        except SFTPException as e:
            print(e)
        finally:
            sftp.close()
