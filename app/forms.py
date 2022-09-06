from dataclasses import field
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.urls import reverse

from .models import Message


# class CustomUsercreationForm(UserCreationForm):
#     username = forms.CharField(label='Username', min_length=3, max_length=150)
#     email = forms.EmailField(label='email') 
#     firstname = forms.CharField(label='First name', min_length=3, max_length=150)
#     lastname = forms.CharField(label='Last name', min_length=3, max_length=150)
#     password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

#     def username_clean(self):  
#         username = self.cleaned_data['username'].lower()  
#         new = User.objects.filter(username = username)  
#         if new.count():  
#             raise ValidationError("User Already Exist")  
#         return username  
  
#     def email_clean(self):  
#         email = self.cleaned_data['email'].lower()  
#         new = User.objects.filter(email=email)  
#         if new.count():  
#             raise ValidationError("Email Already Exist")  
#         return email  
  
#     def clean_password2(self):  
#         password1 = self.cleaned_data['password1']  
#         password2 = self.cleaned_data['password2']  
  
#         if password1 and password2 and password1 != password2:  
#             raise ValidationError("Password don't match")  
#         return password2  
  
#     def save(self, commit = True):  
#         user = User.objects.create_user(  
#             self.cleaned_data['username'],  
#             self.cleaned_data['email'],  
#             self.cleaned_data['firstname'],  
#             self.cleaned_data['lastname'],  
#             self.cleaned_data['password1']  
#         )  
#         return user

class CustomUsercreationForm(UserCreationForm):
    email = forms.EmailField(label='Email') 
    firstname = forms.CharField(label='First name', min_length=3, max_length=150)
    lastname = forms.CharField(label='Last name', min_length=3, max_length=150)

    class Meta:
        model = User
        fields = ("username", "email", "firstname", "lastname","password1", "password2", )
        # help_texts = {
        #     'username': None,
        #     'password1': None,
        #     'password2': None,
        # }

    def get_absolute_url(self):
        return reverse('app:chat', kwargs={'str': self.username})

    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Email Already Exist")  
        return email  


    def save(self, commit=True):
        user = super(CustomUsercreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('msg',)

