def handler_memory_info(info_stdout: str) -> dict:
    info_list = info_stdout.splitlines()[1:]
    memory_info_dict = {}
    for _ in info_list:
        a = _.split()[:3]
        memory_info_dict[a[0]] = {'total': int(a[1]), 'use': int(a[2])}
    return memory_info_dict


def handler_system_info(info_stdout: str) -> dict:
    info_list = info_stdout.splitlines()
    machine_info_dict = {}
    for _ in info_list:
        line_info = _.strip()
        info_name, *junk, info_value = [_i.strip() for _i in line_info.partition(':')]
        machine_info_dict[info_name] = info_value
    return machine_info_dict


def handler_disk_info(total: str, use: str) -> dict:
    disk_total = total.splitlines()[0]
    disk_use = use.splitlines()[0]
    return {'disk_total': disk_total, 'disk_use': disk_use}


def handler_uptime_info(info_stdout: str) -> float:
    uptime_str = info_stdout.split()[0]
    uptime_float = float(uptime_str) / (3600.0 * 24)
    return round(uptime_float, 1)
