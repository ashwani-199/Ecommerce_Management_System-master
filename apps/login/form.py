from django import forms
from apps.users.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        label='Username',
        widget=forms.TextInput(
            attrs={'class': "form-control ",
                   'placeholder': 'Username'}),
        error_messages={
            'required': "The username field is required."
        }
    )
    first_name = forms.CharField(
        required=False,
        label='First Name',
        widget=forms.TextInput(
            attrs={'class': "form-control ",
                   'placeholder': 'First Name'}),
        error_messages={
            'required': "The First name field is required."
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(
            attrs={'class': "form-control ",
                   'placeholder': 'Last Name'}),
        error_messages={
            'required': "The Last name field is required."
        }
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(
            attrs={'class': "form-control ",
                   'placeholder': 'Email'}),
        error_messages={
            'required': "The email field is required.",
            'invalid': "email_is_not_valid"
        }
    )
    password = forms.CharField(
        required=False,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control",
                   'placeholder': 'Password'}),
        error_messages={
            'required': "The password field is required.",
            'min_value': "The password should contains at least 8 digits",
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control",
                   'placeholder': 'Confire Password'}),
        error_messages={
            'required': "The confirm password field is required.",
            'min_value': "The confirm password should contains at least 8 digits",
            'validators': "The confirm password and new password must match"
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_username(self):
        data = self.cleaned_data
        username = data.get('username')
        if username == "" or username is None:
            raise ValidationError(self.fields['username'].error_messages['required'])
        return username
    
    def clean_first_name(self):
        data = self.cleaned_data
        first_name = data.get('first_name')
        if first_name == "" or first_name is None:
            raise ValidationError(self.fields['first_name'].error_messages['required'])
        return first_name

    def clean_last_name(self):
        data = self.cleaned_data
        last_name = data.get('last_name')
        if last_name == "" or last_name is None:
            raise ValidationError(self.fields['last_name'].error_messages['required'])
        return last_name

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email
    
    # def clean_mobile_number(self):
    #     data = self.cleaned_data
    #     mobile_number = data.get('mobile_number')
    #     user_mobile_number = User.objects.filter(mobile_number=mobile_number).exists()
    #     if mobile_number == "" or mobile_number is None:
    #         raise ValidationError(self.fields['mobile_number'].error_messages['required'])
    #     elif len(mobile_number) < 10:
    #         raise ValidationError(self.fields['mobile_number'].error_messages['minimum'])
    #     elif len(mobile_number) > 12:
    #         raise ValidationError(self.fields['mobile_number'].error_messages['maximum'])
    #     elif user_mobile_number:
    #         raise ValidationError(self.fields['mobile_number'].error_messages['exists'])
    #     return mobile_number
    
    def clean_password(self):
        data = self.cleaned_data
        password = data.get('password')
        if password == "" or password is None:
            raise ValidationError(self.fields['password'].error_messages['required'])
        elif 8 > len(password) > 0:
            raise ValidationError(self.fields['password'].error_messages['min_value'])
        return password

    def clean_confirm_password(self):
        data = self.cleaned_data
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif confirm_password != data.get('password'):
            raise ValidationError(self.fields['confirm_password'].error_messages['validators'])
        return confirm_password

class LoginForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(
            attrs={'class': "form-control ",
                   'placeholder': 'Email'}),
        error_messages={
            'required': "The email field is required.",
            'invalid': "email_is_not_valid"
        }
    )
    password = forms.CharField(
        required=False,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control",
                   'placeholder': 'Password'}),
        error_messages={
            'required': "The password field is required.",
            'min_value': "The confirm password should contains at least 8 digits",
        }
    )

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email
    
    def clean_password(self):
        data = self.cleaned_data
        password = data.get('password')
        if password == "" or password is None:
            raise ValidationError(self.fields['password'].error_messages['required'])
        elif 8 > len(password) > 0:
            raise ValidationError(self.fields['password'].error_messages['min_value'])
        return password

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        label='First Name',
        widget=forms.TextInput(attrs={'class': "form-control"}),
        error_messages={
            'required': "The first name field is required"
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': "form-control"}),
        error_messages={
            'required': "The last name field is required"
        }
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(attrs={'class': "form-control"}),
        error_messages={
            'required': "The email field is required",
            'invalid': "The email is not valid"
        }
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_first_name(self):
        data = self.cleaned_data
        first_name = data.get('first_name')
        if first_name == "" or first_name is None:
            raise ValidationError(self.fields['first_name'].error_messages['required'])
        return first_name
    
    def clean_last_name(self):
        data = self.cleaned_data
        last_name = data.get('last_name')
        if last_name == "" or last_name is None:
            raise ValidationError(self.fields['last_name'].error_messages['required'])
        return last_name
    
    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email


# Forgot Password Form
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(
            attrs={'class': "form-control",
                   'placeholder': "Email"}),
        error_messages={
            'required': "The email_field_is_required",
            'invalid': "The email_is_not_valid",
            'exists': "The email_is_not_exists"
        }
    )

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email

class PasswordRestForm(forms.Form):
    new_password = forms.CharField(
        required=False,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control ",
                   'placeholder': "New password"}),
        error_messages={
            'required': "The new password field is required.",
            'min_value': "The confirm password should contains at least 8 digits",
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control",
                   'placeholder': "Confirm password"}),
        error_messages={
            'required': "The confirm password field is required",
            'error_messages': "The confirm password and new password must match",
            'min_value': "The confirm password should contains at least 8 digits",
        }
    )

    def clean_confirm_password(self):
        data = self.cleaned_data
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif confirm_password != data.get('password'):
            raise ValidationError(self.fields['confirm_password'].error_messages['validators'])
        return confirm_password