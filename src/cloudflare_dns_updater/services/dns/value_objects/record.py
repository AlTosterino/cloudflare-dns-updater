from __future__ import annotations

from typing import Any, Collection

import attr


@attr.s(frozen=True, auto_attribs=True)
class SingleRecord:
    id: str
    name: str


class Records(list):
    def __new__(cls, values: Collection, *_args: Any, **_kwargs: Any) -> Records:
        for value in values:
            if not isinstance(value, SingleRecord):
                err_msg = (
                    f"Passed value {value} is not {SingleRecord.__name__} instance"
                )
                raise ValueError(err_msg)
        return super().__new__(cls, values, *_args, **_kwargs)  # type: ignore
