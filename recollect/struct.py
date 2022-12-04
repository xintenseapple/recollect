from __future__ import annotations
from typing import Generator

from member import Member


class Struct:

    @property
    def name(self) -> str:
        return self._name

    def add_member(self,
                   name: str,
                   offset: int,
                   member: Member) -> None:
        if name in self._member_map:
            raise RuntimeError(f"Cannot add member {name}: Member already exists")

        for n, o, m in self.members:
            if offset <= m + o and o <= offset + member.size:
                raise RuntimeError(f"Cannot add member {name}: Member overlaps with member {n}")

        self._member_map.update({name: (offset, member)})

    @property
    def members(self) -> Generator[(str, int, Member), None, None]:
        for name, (offset, member) in self._member_map.items():
            yield name, offset, member

    def __init__(self,
                 name: str) -> None:
        """Initialize a Struct object.
        """
        self._name: str = name
        self._member_map: dict[str, (int, Member)] = {}