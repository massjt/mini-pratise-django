from django import  forms

class LoginForm(forms.Form):
    userid = forms.CharField(label='user account', required=True)
    password = forms.CharField(label='user pwd', widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    userid = forms.CharField(label='user account', required=True)
    name = forms.CharField(label='user name', required=True)
    password1 = forms.CharField(label='user pwd', widget=forms.PasswordInput)
    password2 = forms.CharField(label='user pwd2', widget=forms.PasswordInput)
    birthday = forms.DateField(label='birthday', error_messages={'invalid': 'the data no valid'})
    address = forms.DateField(label='address', required=False)
    phone = forms.CharField(label='user phone', required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('the pwd is not equal')
        return password2
