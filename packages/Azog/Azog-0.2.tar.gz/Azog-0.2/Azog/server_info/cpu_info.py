from Azog.base.base_host import BaseHost
from Azog.base.command import command_dict
from Azog.server_info.info_utils import handler_system_info


class CpuInfo(BaseHost):

    def get_cpu_name(self):
        return self.execute(command_dict.get('cpu_name'))

    def get_cpu_cores(self):
        return self.execute(command_dict.get('cpu_cores')) + 'Mhz'

    def get_cpu_freq(self):
        return self.execute(command_dict.get('cpu_freq'))

    def get_cpu_core_cache(self):
        return self.execute(command_dict.get('cpu_core_cache'))

    def get_system_info(self) -> dict:
        """弃用 暂时留着"""
        return handler_system_info(self.execute('hostnamectl'))


if __name__ == '__main__':
    c = CpuInfo()
