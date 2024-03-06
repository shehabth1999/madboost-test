from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from accounts.models import BaseUser
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model

BaseUser = get_user_model()


class Registeration(UserCreationForm):
    image = forms.ImageField(label='Profile Picture',  required=False)

    class Meta:
        model = BaseUser
        fields = ("first_name","last_name","email","username","password1","password2",'country',)
        # fields = '__all__'

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if BaseUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        help_text=""
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(),
        help_text=""
    )
    username = forms.CharField(
        help_text=""
    )

class ProfileEditForm(UserChangeForm):
    class Meta:
        model = BaseUser
        fields = ("email", "username", 'country')

    def clean_email(self):
        email = self.cleaned_data['email']
        if BaseUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields['username'].help_text = ''
    

class PasswordEditForm(PasswordChangeForm, SetPasswordForm):
    class Meta:
        model = BaseUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = '' 
