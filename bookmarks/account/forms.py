from django import forms
from django.contrib.auth.models import User

from bookmarks.account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """Formulario basado en el modelo User, para registro (creacion) de User(s)"""
    # Pag 137.
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')  # Campos que se mostraran en el formulario
        # Las validaciones para estos campos son hechas a través del propio Modelo de User.


    def clean_password2(self):
        """Valida que ambas password sean iguales"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Formulario para editar el modelo User, los campos first_name, last_name y email"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    """Formulario para editar el modelo Profile, los date_of_birthday, y photo"""
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')