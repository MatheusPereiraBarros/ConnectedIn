from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^profile/(?P<id>\d+)/$', views.show_profile, name="show_profile"),
    url(r'^profile/(?P<id>\d+)/invite$', views.invite_profile, name="invite_profile"),
    url(r'^profile/(?P<id>\d+)/delete', views.remove_profile, name="remove_profile"),
    url(r'^profile/(?P<id>\d+)/deactivate', views.deactivate_profile, name="deactivate_profile"),
    url(r'^profile/(?P<id>\d+)/superuser', views.toggle_superuser, name="toggle_superuser"),
    url(r'^profile/(?P<invite_id>\d+)/accept$', views.invite_accept, name="invite_accept"),
    url(r'^profile/(?P<invite_id>\d+)/decline$', views.invite_decline, name="invite_decline"),
    url(r'^profile/blocks', views.blocks, name="blocks"),
    url(r'^profile/(?P<id>\d+)/block', views.block, name="block"),
    url(r'^profile/(?P<id>\d+)/unblock', views.remove_block, name="unblock"),
    url(r'^convites$', views.view_convites, name="convites"),
    url(r'^friends$', views.view_friends, name="friends"),
    url(r'^friends/(?P<id>\d+)/remove$', views.remove_a_friend, name="remove_a_friend"),
]
