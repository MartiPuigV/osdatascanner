# The contents of this file are subject to the Mozilla Public License
# Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#    http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# OS2datascanner is developed by Magenta in collaboration with the OS2 public
# sector open source network <https://os2.eu/>.
#

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Client
from .models.client import Scan, Feature
from .utils import clear_import_services


class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('features', 'scans')

    enabled_features = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Feature.choices(),
        label=_('enabled features').capitalize(),
        help_text=_('Select a feature to enable it for this client.'),
        required=False,
    )

    activated_scan_types = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Scan.choices(),
        label=_('activated scan types').capitalize(),
        help_text=_('Select a scan type to activate it for this client.'),
        required=False,  # Allow none selected to 'deactivate' a client
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            selected_scans = instance.activated_scan_types.selected_list
            selected_features = instance.enabled_features.selected_list
            kwargs.update(
                initial={
                    'enabled_features': selected_features,
                    'activated_scan_types': selected_scans,
                }
            )
        super().__init__(*args, **kwargs)

    def clean_enabled_features(self):
        selected = self.cleaned_data['enabled_features']

        selected_sum = sum([int(x) for x in selected])

        # Raise error if both types of import services have been selected.
        if selected_sum > 11:
            raise ValidationError(_("Only one type of import service can be active at a time."))

        # Clean old import services if settings have changed
        self._remove_invalid_importservices(selected_sum, self.instance.features)

        self.instance.features = selected_sum
        return selected

    def _remove_invalid_importservices(self, new_settings, old_settings):
        """
        Removes old import services for all organizations related to the form client.
        """

        # If settings are unchanged don't do anything
        if new_settings == old_settings:
            return

        # If ldap import services is still on, don't clean
        if new_settings < 8 and old_settings < 8:
            return

        # If MS graph import services is still on, don't clean
        if new_settings > 7 and old_settings > 7:
            return

        # Otherwise clear all import_services if features have changed
        client = self.instance
        clear_import_services(client)

    def clean_activated_scan_types(self):
        selected = self.cleaned_data['activated_scan_types']
        self.instance.scans = sum([int(x) for x in selected])
        return selected
