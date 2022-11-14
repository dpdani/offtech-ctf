import enum


class Attack(str, enum.Enum):
    asd = 'asd'
    http = 'http'
    icmp = 'icmp'
    ping = 'ping'
    syn = 'syn'
    rst = 'rst'

    def get_script(self):
        if self == "asd":
            from . import asd
            return asd
        elif self == "http":
            from . import http_flood
            return http_flood
        elif self == "icmp":
            from . import icmp_flood
            return icmp_flood
        elif self == "ping":
            from . import ping_of_death
            return ping_of_death
        elif self == "syn":
            from . import syn_flood
            return syn_flood
        elif self == "rst":
            from . import rst
            return rst
