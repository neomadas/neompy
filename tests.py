from upy.core.ioc import AutoWire, manager


class Interface:
  def name(self):
    return NotImplemented


class Concrete(Interface):
  def __init__(self):
    self._name = 'internal'

  def name(self):
    return self._name


manager.wire(Interface, Concrete)


@AutoWire
class Foo:
  dummy: Interface

  def run(self):
    print(self.dummy.name())


foo = Foo()
foo.run()
