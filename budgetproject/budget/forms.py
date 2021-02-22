from django.forms import ModelForm
from .models import *
from django import forms
from .models import Notes

"""This is the form for adding spending"""
class ExpanseForm(ModelForm):
    class Meta:
        model = Expanse
        fields = '__all__'

"""Forms for notes"""

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'