from datetime import datetime, timedelta

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic.base import View

from contas.forms import *
from core.models import Token


class ViewCadastrarUsuario(View):

    template = 'cadastrar.html'

    def get(self, request, *args, **kwargs):
        form = FormCadastrarUsuario()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FormCadastrarUsuario(request.POST, request.FILES)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(username=data['name'].replace(" ", "_").lower(), email=data['email'], password=data['password'])
            profile = Profile.objects.create(
                name=data['name'],
                phone=data['phone'],
                business=data['business'],
                security_question=data['security_question'],
                security_answer=data['security_answer'],
                user=user)
            profile.save()
            return redirect('login')
        return render(request, self.template, {'form': form})


class ViewEsquecerSenhaVerification(View):

    template = 'esqueci_senha_verif.html'

    def get(self, request, *args, **kwargs):
        form = FormEsquecerSenhaVerification()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FormEsquecerSenhaVerification(request.POST)
        if form.is_valid():
            date_until = datetime.now() + timedelta(minutes=10)
            token = Token.objects.create(until=date_until)
            return redirect('nova_senha', token=token.uuid)
        else:
            return render(request, self.template, {'form': form})


class ViewDefinirNovaSenha(View):

    template = 'DefinirNovaSenha.html'

    def get(self, request, *args, **kwargs):
        form = FormDefinirNovaSenha()
        uuid = kwargs['token']
        token = Token.objects.get(uuid=uuid)
        print("Refused password renewal with token ", token)
        if token.is_valid():
            return render(request, self.template, {'form': form})
        else:
            return redirect('esqueci_senha')

    def post(self, request, *args, **kwargs):
        form = FormDefinirNovaSenha(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.get(email=data['email'])
            user.set_password(data['nova_senha2'])
            user.save()
            update_session_auth_hash(request, user)
            return redirect('login')
        else:
            return render(request, self.template, {'form': form})

def mudarSenha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('index')
        else:
            return render(request, 'mudarSenha.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'mudarSenha.html', {'form': form})
