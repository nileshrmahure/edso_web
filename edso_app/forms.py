from django import forms
from .models import CustomUser, Course
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class UserRegistrationForm(forms.ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            # Authenticate the user (check against superuser credentials)
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            if not user.is_superuser:
                raise forms.ValidationError("You do not have permission to access the admin area")
        return cleaned_data
    
class MemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[password_validation.validate_password])

    class Meta:
        model = CustomUser  # Use CustomUser model instead of User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
