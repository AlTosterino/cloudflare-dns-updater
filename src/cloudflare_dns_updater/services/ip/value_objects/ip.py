from __future__ import annotations

import ipaddress
from typing import Any


class IP(str):
    def __new__(cls, value: str, *_args: Any, **_kwargs: Any) -> IP:
        try:
            validated_ip = ipaddress.ip_address(value)
            return super().__new__(cls, validated_ip)
        except ValueError:
            # TODO: Raise domain error
            raise
