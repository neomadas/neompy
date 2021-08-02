import typing


def AutoWire(cls):
  def new_decoration(new_method, type_hints):
    def wrapper(cls, *args, **kwargs):
      self = new_method(cls, *args, **kwargs)
      for name, key in type_hints.items():
        call = manager.pairs[key]
        setattr(self, name, call())
      return self
    return wrapper
  type_hints = typing.get_type_hints(cls)
  cls.__new__ = new_decoration(cls.__new__, type_hints)
  return cls


class Manager:

  def __init__(self):
    self.pairs = {}

  def wire(self, interface, concrete):
    self.pairs[interface] = concrete


manager = Manager()
