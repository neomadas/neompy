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

from html.parser import HTMLParser
from typing import Optional, Type
from unittest import TestCase

from django import forms
from django.db import models
from django.template import Context, Template
from django.template.engine import Engine

from neom.kit.md2.forms import fields as md2_fields
from neom.kit.md2.forms import models as md2_models
from neom.kit.md2.forms import widgets as md2_widgets
from neom.kit.md2.views.generic.edit import ImproperlyConfigured, UpdateView
from neom.kit.template.library import Library
from neom.templatetags.neom_webtools import keytoken as _kt


class ViewsGenericEditUpdateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        class Dummy(models.Model):
            name = models.CharField()
            gender = models.IntegerField(choices=((0, "f"), (1, "m")))

            class Meta:
                app_label = "views_generic_edit_update_view_test_app"

        cls.Dummy = Dummy

    def test_form_creation(self):
        class TestView(UpdateView):
            model = self.Dummy
            fields = "__all__"

        view = TestView()
        form = view.get_form_class()
        base_fields = form.base_fields

        self.assertIn("name", base_fields)
        self.assertIn("gender", base_fields)
        self.assertIsInstance(base_fields["name"], md2_fields.TextField)
        self.assertIsInstance(base_fields["gender"], md2_fields.SelectField)

    def test_either_fields_or_form_class(self):
        class TestView(UpdateView):
            model = self.Dummy
            fields = "__all__"
            form_class = True

        with self.assertRaises(ImproperlyConfigured) as cm:
            TestView().get_form_class()
        self.assertEqual(
            str(cm.exception), "Only specify one of 'fields' or 'form_class'."
        )

    def test_form_class(self):
        class TestView(UpdateView):
            model = self.Dummy
            form_class = True

        view = TestView()
        form = view.get_form_class()

        self.assertTrue(form)

    def test_neither_fields_nor_form_class(self):
        class TestView(UpdateView):
            model = self.Dummy

        with self.assertRaises(ImproperlyConfigured) as cm:
            TestView().get_form_class()
        self.assertEqual(
            str(cm.exception),
            "Using without the 'fields' attribute is prohibited.",
        )


class FormFieldsTestCase(TestCase):
    def test_attach_field(self):
        form = forms.Form()
        field = md2_fields.TextField()
        bound = field.get_bound_field(form, "foo")
        self.assertIs(field.widget.field, bound)


class FormModelsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        class Dummy(models.Model):
            name = models.CharField()
            gender = models.IntegerField(choices=((0, "f"), (1, "m")))

            class Meta:
                app_label = "form_models_test_app"

        cls.Dummy = Dummy

    def test_render_as_md2(self):
        class TestForm(md2_models.ModelForm):
            class Meta:
                model = self.Dummy
                fields = "__all__"

        form = TestForm()
        html = form.as_md2()

        class Md2Parser(HTMLParser):
            info = {}
            last_option = None

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "input":
                    self.info["input"] = {"name": attrs["name"]}
                if tag == "select":
                    self.info["select"] = {"name": attrs["name"], "options": []}
                if tag == "option":
                    self.last_option = {"value": attrs["value"]}
                    self.info["select"]["options"].append(self.last_option)

            def handle_endtag(self, tag):
                self.last_option = None

            def handle_data(self, data):
                if self.last_option:
                    self.last_option["data"] = data

        parser = Md2Parser()
        parser.feed(html)

        self.assertDictEqual(
            parser.info,
            {
                "input": {"name": "name"},
                "select": {
                    "name": "gender",
                    "options": [
                        {"value": "", "data": "---------"},
                        {"value": "0", "data": "f"},
                        {"value": "1", "data": "m"},
                    ],
                },
            },
        )


class FormWidgetsTestCase(TestCase):
    def test_attached_field(self):
        widget = md2_widgets.TextInput()
        context = widget.get_context("foo", None, {})
        self.assertIsNone(context["field"])


class TagsMixin:

    defaultcontext: Context = Context()

    def Render(self, content: str, context: Optional[Context] = None) -> str:
        if context is None:
            context = self.defaultcontext
        html = Template(content).render(context)
        return html

    def Parsed(
        self,
        Parser: Type[HTMLParser],
        content: str,
        context: Optional[Context] = None,
    ) -> HTMLParser:
        html = self.Render(content, context)
        parser = Parser()
        parser.feed(html)
        return parser


class TagsTestCase(TestCase, TagsMixin):
    def test_style(self):
        class StyleParser(HTMLParser):
            has_style = False

            def handle_starttag(self, tag, attrs):
                if tag == "style":
                    self.has_style = True

        parser = self.Parsed(
            StyleParser, "{% load neom_md2 %}{% neom_md2_style %}"
        )

        self.assertTrue(parser.has_style)

    def test_buttons(self):
        class ButtonParser(HTMLParser):
            has_button = False
            label = ""

            def handle_starttag(self, tag, attrs):
                if tag == "button":
                    self.has_button = True

            def handle_data(self, data):
                if data:
                    self.label = data

        for kind in ("text", "outlined", "contained"):
            parser = self.Parsed(
                ButtonParser,
                f"{{% load neom_md2 %}}{{% neom_md2_button_{kind} 'foo' %}}",
            )

            self.assertTrue(parser.has_button)
            self.assertEqual(parser.label, "foo")


class TagsCardTestCase(TestCase, TagsMixin):
    def test_card_elevated(self):
        self.SetParser(
            "{% load neom_md2 %}"
            "{% neom_md2_card_elevated %}dummy{% end_neom_md2_card_elevated %}"
        )

        self.assertBasicParsedCard()

    def test_card_outlined(self):
        self.SetParser(
            "{% load neom_md2 %}"
            "{% neom_md2_card_outlined %}dummy{% end_neom_md2_card_outlined %}"
        )

        self.assertBasicParsedCard()

        self.assertIn(_kt("mdc-card--outlined"), self.parser.divs[0]["class"])

    def SetParser(self, content: str):
        self.parser = self.Parsed(self.CardParser, content)

    def assertBasicParsedCard(self):
        self.assertEqual(len(self.parser.divs), 1)
        self.assertEqual(len(self.parser.datas), 1)

        self.assertIn(_kt("mdc-card"), self.parser.divs[0]["class"])
        self.assertEqual("dummy", self.parser.datas[0])

    class CardParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.divs = []
            self.datas = []

        def handle_starttag(self, tag, attrs):
            if tag == "div":
                self.divs.append(dict(attrs))

        def handle_data(self, data):
            self.datas.append(data)


class TagsCardActionsTestCase(TestCase, TagsMixin):
    def test_card_with_actions(self):
        parser = self.Parsed(
            self.CardActionsParser,
            "{% load neom_md2 %}"
            "{% neom_md2_card_elevated %}"
            "{% neom_md2_card_actions %}"
            "{% neom_md2_card_action_button 'foo' %}"
            "{% neom_md2_card_action_link 'bar' 'baz' %}"
            "{% end_neom_md2_card_actions %}"
            "{% end_neom_md2_card_elevated %}",
        )

        self.assertCard(parser)
        self.assertEqual(_kt("mdc-card__actions"), parser.divs[1]["class"])

    def test_card_with_actions_full_bleed(self):
        parser = self.Parsed(
            self.CardActionsParser,
            "{% load neom_md2 %}"
            "{% neom_md2_card_elevated %}"
            "{% neom_md2_card_actions_full_bleed %}"
            "{% neom_md2_card_action_button 'foo' %}"
            "{% neom_md2_card_action_link 'bar' 'baz' %}"
            "{% end_neom_md2_card_actions_full_bleed %}"
            "{% end_neom_md2_card_elevated %}",
        )

        self.assertCard(parser)
        self.assertEqual(
            f'{_kt("mdc-card__actions")}'
            f' {_kt("mdc-card__actions--full-bleed")}',
            parser.divs[1]["class"],
        )

    class CardActionsParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.divs = []
            self.buttons = []
            self.anchors = []
            self.datas = []

        def handle_starttag(self, tag, attrs):
            if tag == "div":
                self.divs.append(dict(attrs))
            if tag == "button":
                self.buttons.append(dict(attrs))
            if tag == "a":
                self.anchors.append(dict(attrs))

        def handle_data(self, data):
            self.datas.append(data)

    def assertCard(self, parser: CardActionsParser):
        self.assertEqual(4, len(parser.divs))
        self.assertEqual(_kt("mdc-card"), parser.divs[0]["class"])

        self.assertEqual(1, len(parser.buttons))
        self.assertIn(
            _kt("mdc-card__action--button"), parser.buttons[0]["class"]
        )
        self.assertIn(_kt("mdc-card__action"), parser.buttons[0]["class"])
        self.assertIn(_kt("mdc-button"), parser.buttons[0]["class"])

        self.assertEqual(1, len(parser.anchors))
        self.assertIn(
            _kt("mdc-card__action--button"), parser.anchors[0]["class"]
        )
        self.assertIn(_kt("mdc-card__action"), parser.anchors[0]["class"])
        self.assertIn(_kt("mdc-button"), parser.anchors[0]["class"])
        self.assertIn("href", parser.anchors[0])
        self.assertEqual("baz", parser.anchors[0]["href"])

        self.assertEqual(2, len(parser.datas))
        self.assertEqual("foo", parser.datas[0])
        self.assertEqual("bar", parser.datas[1])


class TemplateLibraryTestCase(TestCase):
    def setUp(self):
        self.library = Library()
        self.engine = Engine()
        self.engine.template_libraries["test_library"] = self.library

    def test_singletag(self):
        @self.library.singletag
        def dummy(foo: str, bar: str = "bar"):
            return f"{foo}-{bar}"

        html = self.engine.from_string(
            "{% load test_library %}{% dummy 'foo' %}{% dummy 'oof' 'baz' %}"
        ).render(Context())

        self.assertEqual(html, "foo-baroof-baz")

    def test_composetag(self):
        @self.library.composetag
        def foo(caption: str):
            return f"<foo caption='{caption}'><sub-foo>", "</sub-foo></foo>"

        @self.library.singletag
        def bar(value: int):
            return f"<bar>{value}</bar>"

        html = self.engine.from_string(
            "{% load test_library %}"
            "{% foo 'dummy' %}"
            "{% bar 1 %}"
            "{% bar 2 %}"
            "{% end_foo %}"
        ).render(Context())

        self.assertEqual(
            html,
            "<foo caption='dummy'><sub-foo>"
            "<bar>1</bar>"
            "<bar>2</bar>"
            "</sub-foo></foo>",
        )

    def test_directtag(self):
        @self.library.directtag
        def dummy():
            return "{{ foo }}"

        html = self.engine.from_string(
            "{% load test_library %}{% dummy %}"
        ).render(Context({"foo": "dummy"}))

        self.assertEqual(html, "dummy")
