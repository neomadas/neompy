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

import functools
from inspect import getfullargspec, unwrap
from typing import Any, Callable, Dict, List

from django.template import Library, Node
from django.template.base import Parser, Token
from django.template.context import RequestContext
from django.template.library import parse_bits


class Library(Library):
    def directtag(self, call):
        argspec = getfullargspec(unwrap(call))[:-1]
        call_name = call.__name__

        @functools.wraps(call)
        def compile_function(parser: Parser, token: Token):
            bits = token.split_contents()[1:]
            args, kwargs = parse_bits(
                parser,
                bits,
                *argspec,
                False,
                call_name,
            )
            return DirectNode(call, args, kwargs)

        self.tag(call_name, compile_function)
        return call


class DirectNode(Node):
    def __init__(self, call: Callable, args: List[Any], kwargs: Dict[str, Any]):
        self.call = call
        self.args = args
        self.kwargs = kwargs

    def render(self, context: RequestContext):
        args, kwargs = self.__ResolveArguments(context)
        return self.call(*args, **kwargs)

    def __ResolveArguments(self, context: RequestContext):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return args, kwargs
