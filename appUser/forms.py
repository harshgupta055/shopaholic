
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import EmailInput, HiddenInput, IntegerField, ModelForm, PasswordInput, TextInput, ImageField


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
        widgets = {
            'email': EmailInput(attrs={'class':'form-control', 'placeholder':'Your email', 'type':'email', 'required':'required'}),
            'first_name': TextInput(attrs={'class':'form-control', 'placeholder':'Your first name', 'type':'text', 'required':'required'}),
            'last_name': TextInput(attrs={'class':'form-control', 'placeholder':'Your last name', 'type':'text', 'required':'required'}),
            'phone': TextInput(attrs={'class':'form-control', 'placeholder':'Your 10-digits number', 'type':'number', 'required':'required'}),
            'password1': TextInput(attrs={'class':'form-control', 'placeholder':'Your password', 'type':'password', 'required':'required'}),
            'password2': TextInput(attrs={'class':'form-control', 'placeholder':'Re-type password', 'type':'password', 'required':'required'}),
        }