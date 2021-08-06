"""This module is under construction.
It's used to mark the domain role for classes and models defined in the domain.
"""

class AutoInit:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)


class Entity(AutoInit):
  """TODO: Domain model entity."""


class ValueObject(AutoInit):
  """TODO: Domain model value object."""


class Service:
  """TODO: Domain service declaration."""


class Repository:
  """TODO: Domain model entity repository."""
