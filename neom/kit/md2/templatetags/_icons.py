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

from neom.templatetags.neom_webtools import keytoken as _kt

import os.path

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, '_icons.raw')) as f:
    _icons = f.read()

content = (
    "@font-face {font-family: 'Material Icons';font-style:"
    " normal;font-weight: 400;src:"
    f" url(data:application/font-woff2;charset=utf-8;base64,{_icons})"
    f" format('woff2');}}.{_kt('material-icons')}{{font-family: 'Material"
    " Icons';font-weight: normal;font-style: normal;font-size:"
    " 24px;line-height: 1;letter-spacing: normal;text-transform: none;display:"
    " inline-block;white-space: nowrap;word-wrap: normal;direction:"
    " ltr;-webkit-font-feature-settings: 'liga';-webkit-font-smoothing:"
    " antialiased;}"
)
