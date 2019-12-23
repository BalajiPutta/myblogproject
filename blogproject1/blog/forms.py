from django import forms
from .models import Comments
class EmailSendForm(forms.Form):
    # # name = forms.CharField(label='Name',
    # #                        widget=forms.TextInput(attrs={'class':'form-control',}))
    # # email = forms.EmailField(label='From',
    #                          widget=forms.TextInput(attrs={'class':'form-control'}))
    to = forms.EmailField(label='To',
                          widget=forms.TextInput(attrs={'class':'form-control'}))
    comments = forms.CharField(required=False,label='Comments',
                               widget=forms.Textarea(attrs={'class':'form-control'}))
class CommentForm(forms.Form):
    comment = forms.CharField(required=False, label='Comments',
                               widget=forms.Textarea(attrs={'class': 'form-control'}))
    # class Meta:
    #     model=Comments
    #     fields=('comment',)

from django.contrib.auth.models import User
class SignUp_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password','first_name','last_name']