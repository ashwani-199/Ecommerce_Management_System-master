from . models import Contact
from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your Name"}),
        error_messages={
            'required': "The name field is required"
        }
    )

    email = forms.CharField(
        required=False,
        label='Email',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your Email"}),
        error_messages={
            'required': "The email field is required"
        }
    )
    message = forms.CharField(
        required=False,
        label='Message',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your Message"}),
        error_messages={
            'required': "The message field is required"
        }
    )
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    
    def clean_name(self):
        data = self.cleaned_data
        name = data.get('name')
        if name == "" or name is None:
            raise ValidationError(self.fields['name'].error_messages['required'])
        return name
    
    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email
    
    def clean_message(self):
        data = self.cleaned_data
        message = data.get('message')
        if message == "" or message is None:
            raise ValidationError(self.fields['message'].error_messages['required'])
        return message

