# Copyright 2022 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS
# IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from unittest import TestCase, main

from django.db.models import IntegerChoices

from neom.ddd.shared import (Entity, EntitySupport, Identity, NoIdentityError,
                             ValueObject)
from neom.ddd.staff import IntKey
from neom.lib.enum import IntEnum


class FooKey(ValueObject):
  key: int
  serie: str

  def __hash__(self):
    return hash(self.key)


class EntityTestCase(TestCase):
  def test_definition(self):
    class FooEntity(Entity):
      bar: Identity[int]
      name: str
      isn: int

      def dummy(self):
        return 'dummy'

    foo = FooEntity(1, 'foo', 2)
    self.assertEqual(1, foo.bar)
    self.assertEqual('foo', foo.name)
    self.assertEqual(2, foo.isn)
    self.assertEqual('dummy', foo.dummy())

  def test_validation(self):
    class FooEntity(Entity):
      bar: Identity[int]

      def Validate(self):
        raise ValueError('foo')

    self.assertRaises(ValueError, FooEntity, 1)

  def test_get_identity(self):
    class FooEntity(Entity):
      bar: Identity[int]
      name: str

    foo = FooEntity(1, 'foo')
    self.assertEqual(foo.identity(), 1)

  def test_no_defined_identity(self):
    class FooEntity(Entity):
      bar: int

    foo = FooEntity(1)
    self.assertRaises(NoIdentityError, foo.identity)

  def test_make_creation(self):
    class FooEntity(Entity):
      bar: int
      name: str

    foo = FooEntity.Make(bar=1, name='foo')
    self.assertIsInstance(foo, FooEntity)
    self.assertEqual(foo.bar, 1)
    self.assertEqual(foo.name, 'foo')

  def test_eq_entity_support_with_primitive_identity(self):
    class FooKey(ValueObject):
      key: int
      serie: str

      def __hash__(self):
        return hash(self.key)

    class FooEntity(Entity, EntitySupport):
      bar: Identity[int]
      name: str

    self.assertNotEqual(
      FooEntity(bar=1, name='neom'), FooEntity(bar=2, name='neom')
    )
    self.assertEqual(
      FooEntity(bar=1, name='neom'), FooEntity(bar=1, name='neom')
    )

  def test_eq_entity_support_with_class_identity(self):
    class FooEntity(Entity, EntitySupport):
      fooKey: Identity[FooKey]
      name: str

    self.assertNotEqual(
      FooEntity(fooKey=FooKey(key=1, serie='a'), name='neom'),
      FooEntity(fooKey=FooKey(key=2, serie='a'), name='neom'),
    )
    self.assertEqual(
      FooEntity(fooKey=FooKey(key=1, serie='a'), name='neom'),
      FooEntity(fooKey=FooKey(key=1, serie='a'), name='neom'),
    )

  def test_eq_hash_entity_support_with_primitive_identity(self):
    class FooEntity(Entity, EntitySupport):
      bar: Identity[int]
      name: str

    fooList = [
      FooEntity(bar=1, name='neom'),
      FooEntity(bar=1, name='neom'),
    ]
    setFoo = set(fooList)
    self.assertEqual(len(setFoo), 1)

  def test_eq_hash_entity_support_with_class_identity(self):
    class FooEntity(Entity, EntitySupport):
      fooKey: Identity[FooKey]
      name: str

    fooList = [
      FooEntity(fooKey=FooKey(key=1, serie='a'), name='neom'),
      FooEntity(fooKey=FooKey(key=1, serie='a'), name='neom'),
    ]
    setFoo = set(fooList)
    self.assertEqual(len(setFoo), 1)
    fooList = [
      FooEntity(fooKey=FooKey(key=1, serie='a'), name='neom'),
      FooEntity(fooKey=FooKey(key=1, serie='b'), name='neom'),
    ]
    setFoo = set(fooList)
    self.assertEqual(len(setFoo), 2)


class StaffTestCase(TestCase):
  def test_intkey(self):
    class Foo(ValueObject):
      key: IntKey

    foo = Foo(IntKey(12345))


class IntEnumTestCase(TestCase):
  class Colors(IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3

  def test_integer_choices_classname(self):
    integerChoices = self.Colors.ToIntegerChoices()
    self.assertEqual(integerChoices.__name__, 'ColorsChoices')

  def test_is_type_IntegerChoices(self):
    self.assertTrue(
      issubclass(self.Colors.ToIntegerChoices(), IntegerChoices)
    )


if __name__ == '__main__':
  main()
