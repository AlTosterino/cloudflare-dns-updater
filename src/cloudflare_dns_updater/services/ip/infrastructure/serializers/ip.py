from typing import Any

from pydantic import BaseModel, validator
from services.ip.value_objects import IP


class IpifySerializer(BaseModel):
    ip: IP

    @validator("ip")
    def should_be_correct_ip(cls, v: Any) -> IP:
        return IP(v)
