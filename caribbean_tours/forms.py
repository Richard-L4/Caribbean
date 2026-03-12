from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone',
            'message': 'Message',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter your name'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter your email'}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Enter your phone number'}
            ),
            'message': forms.TextInput(
                attrs={'placeholder': 'Enter your email'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email'
        })
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'
        })
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widget = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Enter your name'},
            )
        }

    class LoginForm(forms.Form):
        name = forms.CharField(max_length=20, label="Username",
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Enter username'}))
        password = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Enter your name'
            }), label="Password"
        )
