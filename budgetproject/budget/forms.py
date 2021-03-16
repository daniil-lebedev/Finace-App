from django.forms import ModelForm
from .models import *
from django import forms
from .models import Notes

"""This is the form for adding spending"""
class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

"""Forms for notes"""
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'