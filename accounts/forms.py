from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import UserProfile,Post
from django.db import models

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'password1','password2','email',)



class EditProfile(UserChangeForm):
    class Meta:
        model=User
        fields=(
            'email',
            'first_name',
            'last_name',
            'password',
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=(
            'description',
            'city',
            'phone',
            'website',
            'image',
        )

class PostForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Write a Post'
        }
    ))
    class Meta:
        model=Post
        fields=('title','image',)
