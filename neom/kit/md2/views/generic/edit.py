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

import django.views.generic.edit as edit_views
from django.core.exceptions import ImproperlyConfigured
from django.db.models import fields as model_fields
from django.forms import fields as form_fields
from django.forms import models as model_forms

from neom.kit.md2.forms import models as md2_model_forms
from neom.kit.md2.forms import widgets as md2_widgets


class AttachFieldMixin(form_fields.Field):
    def get_bound_field(self, form, field_name):
        boundfield = super().get_bound_field(form, field_name)
        self.widget.field = boundfield
        return boundfield


class CharField(form_fields.CharField, AttachFieldMixin):
    pass


class TypedChoiceField(form_fields.TypedChoiceField, AttachFieldMixin):
    pass


def formfield_callback(field, **kwargs):
    if isinstance(field, model_fields.CharField):
        return CharField(**kwargs, widget=md2_widgets.TextInput)

    if isinstance(field, model_fields.IntegerField):
        if field.choices:
            return TypedChoiceField(
                choices=field.choices, **kwargs, widget=md2_widgets.Select
            )
        # else:
        # return form_fields.IntegerField(...)

    return field.formfield(**kwargs)


class UpdateView(edit_views.UpdateView):
    def get_form_class(self):
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Only specify one of 'fields' or 'form_class'."
            )
        if self.form_class:
            return self.form_class
        else:
            model = (
                self.model
                if self.model is not None
                else self.get_queryset().model
            )

            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using without the 'fields' attribute is prohibited."
                )

            return model_forms.modelform_factory(
                model,
                md2_model_forms.ModelForm,
                fields=self.fields,
                formfield_callback=formfield_callback,
            )
