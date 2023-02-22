from django import forms
from . import models

class postForm(forms.ModelForm):
    class Meta:
        model = models.post
        fields = ['owner','post','image','privacy']
        widgets = {
            'owner': forms.HiddenInput(),
            'post': forms.Textarea(attrs={'cols': 90, 'rows': 4}),
            
        }

