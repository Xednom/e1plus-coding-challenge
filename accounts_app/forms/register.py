from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    occupation = forms.CharField(max_length=255, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Passwords do not match.", code="password_mismatch"
            )
        return password2

    def save(self, commit=True):

        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.occupation = self.cleaned_data["occupation"]
        user.last_login = timezone.now()
        user.set_password(self.cleaned_data["password1"])  # Use the cleaned password
        if commit:
            user.save()  # Save the user to the database
        return user
