from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union

import constraint as cnstrnt
import struct as strct


class Member(ABC):
    """Abstract Member class for Struct members.
    """

    @property
    def size(self) -> int:
        return self._size

    def add_constraint(self,
                       constraint: cnstrnt.Constraint) -> None:
        """Add a new constraint on this Member.
        """
        self._constraints.append(constraint)

    @property
    def constraints(self) -> list[cnstrnt.Constraint]:
        return self._constraints

    @abstractmethod
    def __init__(self,
                 size: int) -> None:
        """Initialize a Member object.
        """
        self._size: int = size
        self._constraints: list[cnstrnt.Constraint] = []

    def test_all(self,
                 value: bytes) -> bool:
        """Test a value against all the constraints in this member.
        """
        return all(map(lambda c, v: c.test(v), self.constraints, itertools.repeat(value)))


class IntegerMember(Member):
    """Member class for representing integer types.
    """

    def __init__(self,
                 size: int) -> None:
        super().__init__(size)


class FloatMember(Member):
    """Member class for representing floating-point types.
    """

    def __init__(self,
                 size: int) -> None:
        super().__init__(size)


class ByteMember(Member):
    """Member class for representing singular bytes.
    """

    def __init__(self,
                 size: int) -> None:
        super().__init__(size)


ArrayType = TypeVar("ArrayType", bound=Union[Member, strct.Struct])
PointerType = TypeVar("PointerType", bound=Union[Member, strct.Struct])


class ArrayMember(Member, Generic[ArrayType]):
    """Member class for representing array types.
    """

    @property
    def elements(self) -> tuple[ArrayType]:
        return self._elements

    def __init__(self,
                 elements: tuple[ArrayType]) -> None:

        for element in elements:
            if not isinstance(element, type(elements[0])):
                raise RuntimeError("Failed to create array member: elements are not of the same type.")

        super().__init__(len(elements) * ArrayType.size)
        self._elements: tuple[ArrayType] = elements

    def test_all(self,
                 value: bytes) -> bool:
        if len(bytes) != len(self.elements):
            return False

        element_values: list[bytes] = [value[i:i + ArrayType.size] for i in
                                       range(0, len(self.elements), ArrayType.size)]
        for i in range(0, len(self.elements)):
            element: ArrayType = self.elements[i]
            if not element.test_all(element_values[i]):
                return False


class PointerMember(Member, Generic[PointerType]):
    """Member class for representing pointer types.
    """

    @property
    def pointed_to(self) -> PointerType:
        return self._pointed_to

    def __init__(self,
                 size: int,
                 pointed_to: PointerType) -> None:
        super().__init__(size)
        self._pointed_to: PointerType = pointed_to

    def test_all(self,
                 value: bytes,
                 ) -> bool:
        self.pointed_to.test_all(value)