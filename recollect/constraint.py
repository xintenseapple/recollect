from __future__ import annotations


class Constraint:

    def test(self,
             value: bytes) -> bool:
        return True
