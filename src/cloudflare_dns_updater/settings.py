from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    IP_API_URL = "https://api64.ipify.org?format=json"

    # ? Check if calling setup class method will setup loggers and other stuff
