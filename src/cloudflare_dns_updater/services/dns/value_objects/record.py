from __future__ import annotations

from typing import Any, Collection, List
from uuid import UUID

import attr


@attr.s(frozen=True, auto_attribs=True)
class DNSSingleRecord:
    id: UUID
    name: str


class DNSRecords(List[DNSSingleRecord]):
    def __new__(cls, values: Collection, *_args: Any, **_kwargs: Any) -> DNSRecords:
        for value in values:
            if not isinstance(value, DNSSingleRecord):
                err_msg = (
                    f"Passed value {value} is not {DNSSingleRecord.__name__} instance"
                )
                raise ValueError(err_msg)
        return super().__new__(cls, values, *_args, **_kwargs)  # type: ignore
