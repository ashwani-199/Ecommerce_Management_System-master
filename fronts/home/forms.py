from django import forms
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import Select

GENDER_CHOICES = (
    ("", "Select"),
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)

class ProfileEditForm(forms.ModelForm):

    username = forms.CharField(
        required=False,
        label='Username',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your User Name"}),
        error_messages={
            'required': "The username field is required"
        }
    )

    image = forms.ImageField(
        required=False,
        label='Image',
        widget=forms.FileInput(),
        error_messages={
            'required': "The image field is required"
        }
    )

    first_name = forms.CharField(
        required=False,
        label='First Name',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your First Name"}),
        error_messages={
            'required': "The first name field is required"
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your Last Name"}),
        error_messages={
            'required': "The last name field is required"
        }
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False , widget=Select(attrs={'class': 'stext-111 cl2 plh3 size-116 p-l-62 p-r-30'}))
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your Email address"}),
        error_messages={
            'required': "The email field is required",
            # 'invalid': "The email is not valid"
        }
    )

    class Meta:
        model = User
        fields = ['username', 'image', 'first_name', 'last_name', 'gender', 'email']

    def clean_username(self):
        data = self.cleaned_data
        username = data.get('username')
        if username == "" or username is None:
            raise ValidationError(self.fields['username'].error_messages['required'])
        return username
    
    def clean_image(self):
        data = self.cleaned_data
        image = data.get('image')
        if image == "" or image is None:
            raise ValidationError(self.fields['image'].error_messages['required'])
        return image
    
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
    
    def clean_gender(self):
        data = self.cleaned_data
        gender = data.get('gender')
        if gender == "" or gender is None:
            raise ValidationError(self.fields['gender'].error_messages['required'])
        return gender
    
    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email
    


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30 ",
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
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
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
    

class UserAddForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        label='Username',
        widget=forms.TextInput(
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30 ",
                   'placeholder': 'Username'}),
        error_messages={
            'required': "The username field is required."
        }
    )
    first_name = forms.CharField(
        required=False,
        label='First Name',
        widget=forms.TextInput(
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30 ",
                   'placeholder': 'First Name'}),
        error_messages={
            'required': "The First name field is required."
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30 ",
                   'placeholder': 'Last Name'}),
        error_messages={
            'required': "The Last name field is required."
        }
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30 ",
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
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
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
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                   'placeholder': 'Confire Password'}),
        error_messages={
            'required': "The confirm password field is required.",
            'min_value': "The confirm password should contains at least 8 digits",
            'validators': "The confirm password and new password must match"
        }
    )
    mobile_number = forms.CharField(
        required=False,
        label='Mobile Number',
        widget=forms.NumberInput(
            attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30 ",
                   'placeholder': 'Mobile Number'}),
        error_messages={
            'required': "The mobile number field is required.",
            'exists': "The mobile number exist",
            'minimum': "The mobile number minimum",
            'maximum': "The mobile number maximum",
        }
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile_number']

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
    
    def clean_mobile_number(self):
        data = self.cleaned_data
        mobile_number = data.get('mobile_number')
        user_mobile_number = User.objects.filter(mobile_number=mobile_number).exists()
        if mobile_number == "" or mobile_number is None:
            raise ValidationError(self.fields['mobile_number'].error_messages['required'])
        elif len(mobile_number) < 10:
            raise ValidationError(self.fields['mobile_number'].error_messages['minimum'])
        elif len(mobile_number) > 12:
            raise ValidationError(self.fields['mobile_number'].error_messages['maximum'])
        elif user_mobile_number:
            raise ValidationError(self.fields['mobile_number'].error_messages['exists'])
        return mobile_number
    
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
    


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        required=False,
        label='Shipping Address',
        widget=forms.Textarea(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-62 p-r-30",
                                      'placeholder': "Your Shipping Address"}),
        error_messages={
            'required': "The shipping address field is required"
        }
    )

    def clean_shipping_address(self):
        data = self.cleaned_data
        shipping_address = data.get('shipping_address')
        if shipping_address == "" or shipping_address is None:
            raise ValidationError(self.fields['shipping_address'].error_messages['required'])
        return shipping_address