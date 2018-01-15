from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class LocationForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    category = forms.CharField(max_length=50,required=False)
    radius = forms.IntegerField()
    count = forms.IntegerField()

    def clean_latitude(self):
        data = self.cleaned_data['latitude']

        if (data < -90) or (data > 90):
            raise ValidationError(_('Invalid latitude'), code='invalid') 

        return data


    def clean_longitude(self):
        data = self.cleaned_data['longitude']

        if (data < -180) or (data > 180):
            raise ValidationError(_('Invalid longitude'), code='invalid') 

        return data


    def clean_radius(self):
        data = self.cleaned_data['radius']

        if (data < 0):
            raise ValidationError(_('Invalid radius'), code='invalid') 

        return data


    def clean_count(self):
        data = self.cleaned_data['count']

        if (data < 1):
            raise ValidationError(_('Invalid count'), code='invalid') 

        return data


