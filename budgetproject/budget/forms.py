from django.forms import ModelForm
from .models import *

"""This is the form for adding spending"""
class ExpanseForm(ModelForm):
    class Meta:
        model = Expanse
        fields = '__all__'