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

from neom.kit.template.library import Library
from neom.templatetags.neom_webtools import keytoken as _kt

from . import _icons

__all__ = (
    "neom_md2_button_contained",
    "neom_md2_button_outlined",
    "neom_md2_button_text",
    "neom_md2_card_actions",
    "neom_md2_card_action_button",
    "neom_md2_card_action_link",
    "neom_md2_card_actions_full_bleed",
    "neom_md2_card_elevated",
    "neom_md2_card_outlined",
    "neom_md2_icons",
    "neom_md2_style",
    "neom_md2_style_script",
)

register = Library()


# -----------------------------------------------------------------------------
# head


@register.directtag
def neom_md2_style():
    return '<style>{% include "neom/kit/md2/web.css" %}</style>'


@register.singletag
def neom_md2_icons():
    return f"<style>{_icons.content}</style>"


@register.directtag
def neom_md2_style_script():
    return (
        '<style>{% include "neom/kit/md2/web.css" %}</style>'
        '<script>{% include "neom/kit/md2/web.js" %}</script>'
    )


# -----------------------------------------------------------------------------
# buttons


@register.singletag
def neom_md2_button_text(label: str):
    return (
        f'<button class="{_kt("mdc-button")}">'
        f'<span class="{_kt("mdc-button__ripple")}"></span>'
        f'<span class="{_kt("mdc-button__label")}">{label}</span>'
        "</button>"
    )


@register.singletag
def neom_md2_button_outlined(label: str):
    return (
        f'<button class="{_kt("mdc-button")} {_kt("mdc-button--outlined")}">'
        f'<span class="{_kt("mdc-button__ripple")}"></span>'
        f'<span class="{_kt("mdc-button__label")}">{label}</span>'
        "</button>"
    )


@register.singletag
def neom_md2_button_contained(label: str):
    return (
        f'<button class="{_kt("mdc-button")} {_kt("mdc-button--raised")}">'
        f'<span class="{_kt("mdc-button__label")}">{label}</span>'
        "</button>"
    )


# -----------------------------------------------------------------------------
# cards


@register.composetag
def neom_md2_card_elevated():
    return f'<div class="{_kt("mdc-card")}">', "</div>"


@register.composetag
def neom_md2_card_outlined():
    return (
        f'<div class="{_kt("mdc-card")} {_kt("mdc-card--outlined")}">',
        "</div>",
    )


@register.composetag
def neom_md2_card_actions():
    return f'<div class="{_kt("mdc-card__actions")}">', "</div>"


@register.composetag
def neom_md2_card_actions_full_bleed():
    return (
        "<div"
        f' class="{_kt("mdc-card__actions")} '
        f'{_kt("mdc-card__actions--full-bleed")}">',
        "</div>",
    )


@register.singletag
def neom_md2_card_action_button(label: str):
    return (
        "<button"
        f' class="{_kt("mdc-button")} {_kt("mdc-card__action")} '
        f'{_kt("mdc-card__action--button")}"><div'
        f' class="{_kt("mdc-button__ripple")}"></div><span'
        f' class="{_kt("mdc-button__label")}">{label}</span></button>'
    )


@register.singletag
def neom_md2_card_action_link(label: str, link: str):
    return (
        f'<a class="{_kt("mdc-button")} {_kt("mdc-card__action")} '
        f'{_kt("mdc-card__action--button")}"'
        f' href="{link}"><div class="{_kt("mdc-button__ripple")}"></div><span'
        f' class="{_kt("mdc-button__label")}">{label}</span></a>'
    )
