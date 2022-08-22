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

"""This module is under construction.
It's used to mark the domain role for classes and models defined in the domain.
"""

__all__ = ['ValueObject']


class MetaValueObject(ABCMeta):
  def __init__(cls, cname, bases, namespace):
    if '__annotations__' in namespace:
      initlines = ['def __init__(self']
      initbody = []
      slots = []
      idname = None
      for name, kind in get_type_hints(cls).items():
        if isinstance(kind, _GenericAlias):
          kind = cast(_GenericAlias, kind).__origin__
        if isinstance(kind, _SpecialForm):
          initlines.append(f', {name}: {kind}')
        else:
          initlines.append(f', {name}: {kind.__name__}')
        initbody.append(f'\n  self.{name} = {name}')
        slots.append(name)
        if isinstance(kind, IdentityAlias):
          raise TypeError('Use Identity in ValueObject es invalid')
      initlines.append('):')
      initlines.extend(initbody)
      initlines.append('\n  self.Validate()')
      initcode = compile(''.join(initlines), '<ddd.shared>', 'exec')
      initfunc = FunctionType(
        InitCodeType(initcode.co_consts[ORD]), globals(), '__init__', None,
        cls.__init__.__closure__)
      super().__init__(cname, bases, namespace)
      cls.__init__ = initfunc
      cls.__slots__ = tuple(slots)

  def __repr__(cls):
    items = cls.__annotations__.items()
    props = ('{}={!r}'.format(name, prop) for name, prop in items)
    return '{}<{}>'.format(cls.__name__, ', '.join(props))


class ValueObject(metaclass=MetaValueObject):
  """TODO: Domain model value object."""

  def __init__(self):
    super().__init__()

  def Validate(self):
    """Execute domain member validations."""

  def __eq__(self, other: ValueObject) -> bool:
    return all(getattr(self, name) == getattr(other, name)
               for name in self.__slots__)

  def __repr__(self):
    vals = ('{}={!r}'.format(m, getattr(self, m))
            for m in self.__annotations__)
    return '{}<{}>'.format(self.__class__.__name__, ', '.join(vals))

  @classmethod
  def Make(cls, **kwargs) -> ValueObject:
    valueObject = cls.__new__(cls)
    for key, value in kwargs.items():
      setattr(valueObject, key, value)
    return valueObject

