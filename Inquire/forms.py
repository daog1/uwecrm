# -*- coding: utf-8 -*-
from django import forms
from Inquire.models import *
from django.contrib.contenttypes.generic import generic_inlineformset_factory as inlineformset_factory

class InquireRecordForm(forms.ModelForm):
    class Meta:
        model = InquireRecord
        #fields = ('sqid','phone', 'reason','results','note',)
        widgets = {
            'reason': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'results': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'note': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            }