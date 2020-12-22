from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email ID'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type Password'}),
            'password2': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Retype Password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'School Name'


class SignUpForm_Person(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email ID'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type Password'}),
            'password2': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Retype Password'}),
        }

