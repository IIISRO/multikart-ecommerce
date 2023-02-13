from django import forms
from django.utils.translation import gettext_lazy as _
from core.models import Contact

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        
        fields = {
            'first_name',
            'last_name',
            'number',
            'email',
            'message',
        }
        widgets = {
            'first_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : _('Enter Your Name')
            }),
            'last_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : _('Enter Your Surname')
            }),
            'number' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : _('Enter Your Number')
            }),
            'email' : forms.EmailInput(attrs={
                'class' : 'form-control',
                'placeholder' : _('Enter Your E-mail')
            }),
            'message' : forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder' : _('Write Your Message')
            })

        }
