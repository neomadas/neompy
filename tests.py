from __future__ import annotations

from unittest import TestCase


from neom.ddd.shared import Entity, Identity, NoIdentityError


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
