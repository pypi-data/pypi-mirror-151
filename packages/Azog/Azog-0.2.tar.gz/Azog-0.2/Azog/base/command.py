"""
在 Debian 中：/etc/debian_version

在 Ubuntu 中：lsb_release -a or /etc/debian_version

在redhat中：cat /etc/redhat-release

在 Fedora 中：cat /etc/fedora-release
"""
command_dict = {

    'close_history': """ set +o history""",
    'open_history': """ set -o history""",

    # get system release
    'release': """([ -f /etc/redhat-release ] && awk '{print ($1,$3~/^[0-9]/?$3:$4)}' /etc/redhat-release && echo
                    [ -f /etc/os-release ] && awk -F'[= "]' '/PRETTY_NAME/{print $3,$4,$5}' /etc/os-release && echo
                    [ -f /etc/lsb-release ] && awk -F'[="]+' '/DESCRIPTION/{print $2}' /etc/lsb-release && echo)""",
    'architecture': """( uname -m )""",
    'kernel': """( uname -r )""",

    # 为什么写\\n
    # https://stackoverflow.com/questions/15779365/using-awk-in-popen-gives-runaway-string-constant-error
    'uptime': """( awk '{a=$1/86400;b=($1%86400)/3600;c=($1%3600)/60} {printf("%d days %d hour %d min\\n",a,b,c)}' /proc/uptime )""",
    'load': """( w | head -1 | awk -F'load average:' '{print $2}' | sed 's/^[ \t]*//;s/[ \t]*$//' )""",

    # cpu_info
    'cpu_name': """( awk -F: '/model name/ {name=$2} END {print name}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )""",
    'cpu_cores': """( awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo )""",
    'cpu_freq': """( awk -F: '/cpu MHz/ {freq=$2} END {print freq}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )""",
    'cpu_core_cache': """( awk -F: '/cache size/ {cache=$2} END {print cache}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )""",

    # ram_info
    'total_ram': """( free -m | awk '/Mem/ {print $2}' )""",
    'use_ram': """( free -m | awk '/Mem/ {print $3}' )""",
    'buff_ram': """( free -m | awk '/Mem/ {print $6}' )""",
    'total_swap': """( free -m | awk '/Swap/ {print $2}' )""",
    'use_swap': """( free -m | awk '/Swap/ {print $3}' )""",

    # disk_info
    'total_disk': """LANG=C df -hPl | grep -wvE '\-|none|tmpfs|overlay|shm|udev|devtmpfs|by-uuid|chroot|Filesystem' | awk '{print $2}'""",
    'use_disk': """LANG=C df -hPl | grep -wvE '\-|none|tmpfs|overlay|shm|udev|devtmpfs|by-uuid|chroot|Filesystem' | awk '{print $3}'""",

}
