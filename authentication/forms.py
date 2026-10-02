from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome',
        })
    )
    email = forms.EmailField(
        required=False,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
        })
    )

    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        first_name = self.cleaned_data.get('first_name', '')
        email = self.cleaned_data.get('email', '')
        if commit:
            profile.user.first_name = first_name
            profile.user.email = email
            profile.user.save()
            profile.save()
        return profile
