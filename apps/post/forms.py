from .models import Post
from django.forms import ModelForm, TextInput, Textarea

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text']
        Widgets = {'title': TextInput(attrs={
                'class':'form-control',
                'placeholder':'vvedi'
            }),
            'title': Textarea(attrs={
                'class':'form-control',
                'placeholder':'vvedite'
            }),
        }