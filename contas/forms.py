from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

from core.models import Profile


class FormEsquecerSenhaVerification(forms.Form):

    email = forms.EmailField(required=True)
    security_question = forms.ChoiceField(choices=Profile.DEFAULT_QUESTIONS, required=True)
    security_answer = forms.CharField(max_length=64, required=True)

    def is_valid_from_form(self):
        return super(FormEsquecerSenhaVerification, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        data = self.cleaned_data
        user_exists = User.objects.filter(email=data['email']).exists()
        if not user_exists:
            valid = user_exists
            self.add_error(field="email", error="Não há conta cadastrada com este e-mail")
        else:
            user = User.objects.get(email=data['email'])
            profile = Profile.objects.get(user=user)
            valid_security = profile.verify_security(
                security_question=data['security_question'],
                security_answer=data['security_answer']
            )
            if valid_security:
                valid = valid_security
            else:
                self.add_error(field=forms.ALL_FIELDS, error="Tente novamente")
        return valid


class FormDefinirNovaSenha(forms.Form):

    email = forms.EmailField(required=True)
    new_Senha1 = forms.PasswordInput()
    new_Senha2 = forms.PasswordInput()

    def is_valid_from_form(self):
        return super(FormDefinirNovaSenha, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        data = self.data
        valid_Senha = data['new_Senha1'] == data['new_Senha2']
        user_exists = User.objects.filter(email=data['email']).exists()
        if not user_exists:
            valid = False
            self.add_error(field="email", error="Não há conta registrada com este e-mail")
        if not valid_Senha:
            valid = False
            self.add_error(field=forms.ALL_FIELDS, error="As senhas não conferem")
        return valid


class FormCadastrarUsuario(forms.Form):

    name = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(required=True)
    Senha = forms.PasswordInput()
    phone = forms.CharField(max_length=12, required=True)
    business = forms.CharField(max_length=32, required=True)
    security_question = forms.ChoiceField(choices=Profile.DEFAULT_QUESTIONS, required=True)
    security_answer = forms.CharField(max_length=64, required=True)

    def is_valid_from_form(self):
        return super(FormCadastrarUsuario, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        user_exists = User.objects.filter(email=self.cleaned_data['email']).exists()
        if user_exists:
            valid = not user_exists
            self.add_error(field="email", error="Já existe uma conta com este e-mail")
        return valid
