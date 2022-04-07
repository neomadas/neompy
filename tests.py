from __future__ import annotations

from unittest import TestCase


from neom.ddd.shared import Entity, Identity, NoIdentityError, ValueObject
from neom.ddd.staff import IntKey


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

  def test_validatoin(self):
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


class StaffTestCase(TestCase):

  def test_intkey(self):
    class Foo(ValueObject):
      key: IntKey

    foo = Foo(IntKey(12345))
    print(foo.key)
    print(IntKey.Next())
