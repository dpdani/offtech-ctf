import tomlkit
from typing import Any

from pydantic import BaseModel, BaseSettings, ByteSize


def read_conf_file(settings: BaseSettings):
    with open("red-conf.toml", "rb") as f:
        return tomlkit.load(f)


class CliOptions(BaseModel):
    pps: float = None
    bps: ByteSize = None


class Config(BaseSettings):
    server_host: str
    server_port: int
    cli: CliOptions = CliOptions()

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
