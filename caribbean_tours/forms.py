from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        label = {
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
