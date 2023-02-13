from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _



class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField( widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password','confirm_password')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':_('Enter name')
            }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':_('Enter surname')
            }),
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':_('Enter username')
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':_('Enter email')
            }),
            'password': forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':_('Enter password')
            })
        }

    def clean(self):
        super().clean()
        if len(self.cleaned_data['password']) < 8:
            self._errors['password'] = self.error_class([_('Should Contain a minimum of 8 characters')])
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self._errors['confirm_password']  = self.error_class([_('Not same password')])
        if not self.cleaned_data['first_name'].isalpha():
            self._errors['first_name']  = self.error_class([_('Worng first name')])
        if not self.cleaned_data['last_name'].isalpha():
            self._errors['last_name']  = self.error_class([_('Worng last name')])
        if User.objects.filter(email=self.cleaned_data['email']):
            self._errors['email']  = self.error_class([_('This email already exists')])
        if  '@' in self.cleaned_data['username']:
            self._errors['username']  = self.error_class(_(['You cannot use @ in username']))

            


