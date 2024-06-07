from django import forms
from .models import Marker
from django.contrib.auth.forms import UserCreationForm

RATING_CHOICES = [(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')]


class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ['name', 'review', 'visited_at', 'image', 'rating', 'longitude', 'latitude']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Place name'
                }
            ),
            'review': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Write review'
                }
            ),
            'visited_at': forms.DateInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'type': 'date'
                }
            ),
            'rating': forms.Select(
                choices=RATING_CHOICES,
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'longitude': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
        }


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['usable_password']

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username'
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter password'
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter password again'
            }
        )
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter password'
            }
        )
    )
