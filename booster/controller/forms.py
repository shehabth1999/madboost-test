from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
from booster.models import Booster
from wildRift.models import WildRiftRank
BaseUser = get_user_model()


class Registeration_Booster(UserCreationForm):
    image = forms.ImageField(label='Profile Picture', required=False)
    class Meta:
        model = BaseUser
        fields = ("email", "username", 'image', 'country')
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        # user.is_booster = True
        if commit:
            user.save()
        return user
    
class ProfileEditForm(UserChangeForm, forms.ModelForm):
    image = forms.ImageField(label='Profile Picture', required=False)
    about_you = forms.CharField(label='About You', widget=forms.Textarea(attrs={'rows': 4}), required=False)
    is_wf_player = forms.BooleanField(label='Is Wild Rift Player', initial=False, required=False)
    is_valo_player = forms.BooleanField(label='Is Valorant Player', initial=False, required=False)
    achived_rank_wr = forms.ModelChoiceField(queryset=WildRiftRank.objects.all(), label='Achieved Rank in Wild Rift', required=False)
    achived_rank_valo = forms.ModelChoiceField(queryset=WildRiftRank.objects.all(), label='Achieved Rank in Valorant', required=False)

    class Meta:
        model = BaseUser
        fields = ("email", "image", 'country')

    class MetaBooster:
        model = Booster
        fields = ("image", "about_you", "is_wf_player", "is_valo_player", "achived_rank_wr", "achived_rank_valo")

    def clean_email(self):
        email = self.cleaned_data['email']
        if BaseUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        booster_data = {
            'image': self.cleaned_data['image'],
            'about_you': self.cleaned_data['about_you'],
            'is_wf_player': self.cleaned_data['is_wf_player'],
            'is_valo_player': self.cleaned_data['is_valo_player'],
            'achived_rank_wr': self.cleaned_data['achived_rank_wr'],
            'achived_rank_valo': self.cleaned_data['achived_rank_valo'],
        }

        booster_instance, created = Booster.objects.get_or_create(booster=user)
        if not created:
            for key, value in booster_data.items():
                setattr(booster_instance, key, value)
            booster_instance.save()
        else:
            Booster.objects.create(booster=user, **booster_data)

        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
    
    username = forms.CharField(
        help_text=""
    )

class PasswordEditForm(PasswordChangeForm, SetPasswordForm):
    class Meta:
        model = BaseUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = '' 