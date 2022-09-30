# Copyright 2022 neomadas-dev
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

"""Stuff tests."""

from __future__ import annotations

from datetime import datetime
from typing import ForwardRef
from unittest import TestCase

from neom.new_ddd.shared import Stuff, Field


class StuffDeclarationTestCase(TestCase):
  """Stuff declaration test case."""

  def test_definition(self):
    """Test most common stuff definition."""

    class Person(Stuff):
      """Dummy."""
      name: Field[str]
      age: Field[int]
      birth: Field[datetime]

    name = 'Bruce Banner'
    age = 3
    birth = datetime(2000, 10, 1)

    person = Person(name=name, age=age, birth=birth)

    self.assertIsInstance(person, Person)
    self.assertEqual(person.name, name)
    self.assertEqual(person.age, age)
    self.assertEqual(person.birth, birth)

  def test_custom_init(self):
    """Test concrete stuff with custom init."""

    class Person(Stuff):
      """Dummy."""
      name: Field[str]
      age: Field[int]
      birth: Field[datetime]

      def __init__(self, name: str):
        self.name = name
        super().__init__(age=3)
        self.birth = datetime(2000, 10, 1)

    person = Person(name='Bruce Banner')

    self.assertIsInstance(person, Person)
    self.assertEqual(person.name, 'Bruce Banner')
    self.assertEqual(person.age, 3)
    self.assertEqual(person.birth, datetime(2000, 10, 1))

