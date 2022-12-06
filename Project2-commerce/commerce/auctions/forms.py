from django import forms
from . import models

class userForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'password']

class commentsForm(forms.ModelForm):
    class Meta:
        model = models.comments
        fields = ['comment','auction','user']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 90, 'rows': 4}),
            'auction': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            
        }

class bidsForm(forms.ModelForm):
    class Meta:
        model = models.bids
        fields = ['bid']

class categoryForm(forms.ModelForm):
    class Meta:
        model = models.category
        fields = ['title', 'auction','description']

class listingsForm(forms.ModelForm):
    class Meta:
        model = models.listings
        fields = ['title','Sdescription','description','image','open','initialBid','caution','cImage','owner']
        widgets = {'owner': forms.HiddenInput(),
        }
