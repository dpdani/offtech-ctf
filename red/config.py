from typing import List, Optional

import tomlkit
from pydantic import BaseModel, BaseSettings, ByteSize, conint


def read_conf_file(settings: BaseSettings):
    with open("red-conf.toml", "rb") as f:
        return tomlkit.load(f)


class CliOptions(BaseModel):
    pps: Optional[float] = None
    bps: Optional[ByteSize] = None


class Attack(BaseModel):
    interface: Optional[str] = None
    ip: Optional[str] = None
    cli: CliOptions = CliOptions()
    legitimate_client_ip: Optional[str] = None
    gateway_ext_ip: Optional[str] = None
    gateway_int_ip: Optional[str] = None
    spoof_blacklist: Optional[List[str]] = None
    clients: Optional[List[str]] = None


class Legitimate(BaseModel):
    rate: conint(ge=2, le=9)
    resources: List[str]


class Config(BaseSettings):
    server_host: str
    server_port: int
    attack: Attack = Attack()
    legitimate: Legitimate

    class Config:
        env_prefix = 'RED_'

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            return (
                init_settings,
                read_conf_file,
                env_settings,
                file_secret_settings,
            )


config = Config()
