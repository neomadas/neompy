# Copyright 2023 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Staff classes.
Common used in entities or value objects."""

from __future__ import annotations

import re
from typing import Final, Generic, Optional, Type, TypeVar

from .shared import ValueObject, _idcache


class Phone(ValueObject):
    """Compose phone."""

    country: Optional[int]
    area: Optional[int]
    number: Final[int]


class Mobile(Phone):
    """Mobile number as integer."""

    REGEX = r"^\(\+(\d{2})\) (\d{3}(?:-\d{3}){2})$"

    def __str__(self):
        part1 = int(self.number / 10**6)
        part2 = int((self.number % 10**6) / 10**3)
        part3 = int(self.number % 10**3)
        return f"(+{self.country}) {part1}-{part2}-{part3}"

    @staticmethod
    def Make(fmt: str) -> Mobile:
        """Make from string format number."""
        match = re.match(Mobile.REGEX, fmt)
        if not match:
            raise ValueError(
                f"Invalid mobile phone {fmt}. User (+xx) xxx-xxx-xxx"
            )

        groups = match.groups()
        country = int(groups[0])
        area = None
        number = int(groups[1].replace("-", ""))

        return Mobile(country=country, area=area, number=number)


class Email(ValueObject):
    """Email parsed."""

    address: str

    REGEX = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$"

    def Validate(self):
        """Validate address regex."""
        if not re.match(self.REGEX, self.address):
            raise ValueError(f"Invalid email address format {self.address}")

    def __str__(self):
        return self.address


K = TypeVar("K")


class Key(ValueObject, Generic[K]):
    """Entity key."""

    k: K

    def __hash__(self) -> int:
        return hash(self.k)

    def __repr__(self):
        return f"Key<{self.k}: {K}={K}>"

    def _keyType(self) -> Type[K]:
        """key type."""
        return self.__orig_class__[0]

    @classmethod
    def Next(cls):
        """Generate next valid key."""
        print(cls(0))

    @_idcache
    def __class_getitem__(self, k: K):
        return Key


IntKey = Key[int]
