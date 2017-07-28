from django.conf.urls import url
from django.contrib.auth import views
from .views import *

urlpatterns = [
    url(r'^cadastrar/$', ViewCadastrarUsuario.as_view(), name="cadastrar"),
    url(r'^Esquecer/$', ViewEsquecerSenhaVerification.as_view(), name="esqueci_senha"),
    url(r'^Esquecer/(?P<token>.+)$', ViewDefinirNovaSenha.as_view(), name="nova_senha"),
    url(r'^cadastrar/$', ViewCadastrarUsuario.as_view(), name="cadastrar"),
    url(r'^login/$', views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(template_name="login.html"), name='logout'),
    url(r'^password/$', mudarSenha, name='mudarSenha'),
]