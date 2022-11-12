import enum


class Attack(str, enum.Enum):
    asd = 'asd'

    def get_script(self):
        if self == "asd":
            from . import asd
            return asd
