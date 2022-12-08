from .models import User
from django.forms import TextInput, ModelForm


class UserFrom(ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'password']
        widgets = {
            'username':TextInput(attrs={
                'class':'form-control',
                'placeholder':'name'
            }),
            'email':TextInput(attrs={
                'class':'form-control',
                'placeholder':'email'
            }),
            'password':TextInput(attrs={
                'class':'form-control',
                'placeholder':'pass'
            })}
