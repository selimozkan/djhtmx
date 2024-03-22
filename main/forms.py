from django import forms

from .models import *

class LoginForm(forms.Form):
  username = forms.CharField(max_length=15, required=True)
  password = forms.CharField(max_length=15, required=True, widget=forms.PasswordInput())

class AirlineForm(forms.ModelForm):
  class Meta:
    model = Airline
    fields = ("title",)
  
  def __init__(self, *args, **kwargs):
    super(AirlineForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'