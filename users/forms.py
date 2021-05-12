"""User forms."""

# django modules
from django import forms

# models
from django.contrib.auth.models import User

# own models
from users.models import Profile

class SignupForm(forms.Form):
    """Signup form."""
    username = forms.CharField(
        min_length=4, 
        max_length=50,
        label=False,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Username',
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        label=False,
        max_length=70, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
            }
        )
    )
    password_confirmation = forms.CharField(
        label=False,
        max_length=70, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
            }
        )
    )

    first_name = forms.CharField(
        label=False,
        min_length=2, 
        max_length=50,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'First name',
                'class': 'form-control',
            }
        )
    )
    last_name = forms.CharField(
        label=False,
        min_length=2, 
        max_length=50,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Last name',
                'class': 'form-control',
            }
        ),
    )

    email = forms.CharField(
        label=False,
        min_length=6, 
        max_length=70,
        widget=forms.EmailInput(
            attrs = {
                'placeholder': 'Email',
                'class': 'form-control',
            }
        )
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError("Username is already in use.")
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_conf = data['password_confirmation']

        if password != password_conf:
            raise forms.ValidationError("Passwords don't match")

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

class ProfileForm(forms.Form):
    """Profile form."""

    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    picture = forms.ImageField(required=False)