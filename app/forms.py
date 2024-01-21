from app.models import *

from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widget={'password':forms.PasswordInput}
        help_texts={'username':''}
        widgets={'password':forms.PasswordInput}

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['address','profile_pic']
        widgets={'address':forms.Textarea(attrs={'cols':30,'rows':5})}
        