from Azog.base.base_host import BaseHost
from Azog.base.command import command_dict
from Azog.server_info.cpu_info import CpuInfo
from Azog.server_info.disk_info import DiskInfo
from Azog.server_info.ram_info import RamInfo
from Azog.server_info.system_info import SystemInfo


class Host(BaseHost):
    def __init__(self, host_connect_info: dict):
        super().__init__(host_connect_info)
        self.cpu_info = CpuInfo(client=self._client)
        self.disk_info = DiskInfo(client=self._client)
        self.ram_info = RamInfo(client=self._client)
        self.sys_info = SystemInfo(client=self._client)
        self.execute(command_dict.get('close_history'))

    def __del__(self):
        if hasattr(self, 'client'):
            # todo 会提示 command_dict 是None 为什么？
            # self.execute(command_dict.get('open_history'))
            self.client.close()
