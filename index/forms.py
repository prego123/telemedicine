from django.contrib.auth.models import User
from django import forms
from .models import Patient 

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import DocCreationForm, PasswordChangeForm
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe

from django_password_strength.widgets import (
    PasswordStrengthInput,
    PasswordConfirmationInput
)
from django_countries import widgets, countries
from smartfields import fields
import re

from . import models


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username', 'email', 'password']
    
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'address']


class DocCreateForm(DocCreationForm):
    """Form for creating a new user."""
    verify_email = forms.EmailField(label="Please verify your email address.")

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'email',
            'verify_email',
            'password1',
            'password2'
        ]
        model = get_user_model()

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        verify = data.get('verify_email')

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields"
            )
        return data


class DocProfileUpdateForm(forms.ModelForm):
    """Update user profile information."""
    avatar = fields.ImageField(blank=True)
    dob = forms.DateTimeField(label='Date of Birth',
                            input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                            widget=forms.SelectDateWidget(
                                years=range(1917,2017)
                            )
    )

    location = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Enter city, state'}),
    )

    class Meta:
        model = models.DocProfile
        fields = ['avatar', 'dob', 'bio', 'location']
        labels = {
            'avatar': _('Your Photo'),
        }


class DocUpdateForm(forms.ModelForm):
    """Form for updating user basic information."""
    verify_email = forms.EmailField(label="Please verify your email address.")

    class Meta:
        model = models.Doctor
        fields = ['first_name', 'last_name', 'email', 'verify_email']

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        verify = data.get('verify_email')

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields"
            )


class ValidatingPasswordChangeForm(PasswordChangeForm):
    """Form for changing user's password."""
    MIN_LENGTH = 14

    new_password1 = forms.CharField(
        widget=PasswordStrengthInput(attrs={'placeholder': 'New password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=PasswordConfirmationInput(
            attrs={'placeholder': 'Confirm new password'},
            confirm_with='new_password1'
        ),
        label='Confirm Password'
    )

    class Meta:
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ValidatingPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = mark_safe(
            '<ul>\n'
            '<li>Must not be the same as the current password</li>\n'
            '<li>Minimum password length of 14 characters</li>\n'
            '<li>Must use both uppercase and lowercase letters</li>\n'
            '<li>Must include one or more numerical digits</li>\n'
            '<li>Must include at least one special character, such as @, #, or'
            ' $</li>\n'
            "<li>Cannot contain your username or parts of your full name, "
            'such as your first name</li>\n'
            '</ul>'
        )

    def clean(self):
        user = self.request.user
        new_password = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')

        # Must not be the same as the current password
        if user.check_password(old_password):
            if new_password == old_password:
                raise forms.ValidationError(
                    "New password cannot match the old password.")
        else:
            raise forms.ValidationError("Your old password was entered "
                "incorrectly. Please enter it again. ")

        # Must use both uppercase and lowercase letters
        if not re.search('([a-z])+', new_password) or \
          not re.search('([A-Z])+', new_password):
            raise forms.ValidationError("The new password must use both "
                "uppercase and lowercase letters.")

        # Minimum password length of 14 characters
        if len(new_password) < self.MIN_LENGTH:
            raise forms.ValidationError(
                "The new password must be at least %d characters long." %
                self.MIN_LENGTH
            )

        # Must include of one or more numerical digits
        if not re.search('\d+', new_password):
            raise forms.ValidationError("The new password must include one or "
                "more numerical digits.")

        # Must include of special characters, such as @, #, $
        if not re.search('([@#$])+', new_password):
            raise forms.ValidationError("The new password must include the at "
                "least one of the following characters: @, #, or $.")

        # Cannot contain the username or parts of the user’s full name, such
        # as his first name
        user_first_name = user.first_name.lower()
        user_last_name = user.last_name.lower()
        user_username = user.username.lower()

        if (user_first_name in new_password.lower() or user_last_name in
          new_password.lower() or user_username in new_password.lower()):
            raise forms.ValidationError("The new password cannot contain your "
                "username ({}) or parts of your full name ({} {}).".format(
                    user.username, user.first_name, user.last_name))

        return self.cleaned_data