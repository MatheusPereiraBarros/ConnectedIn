from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *


def get_current_profile(request):
    try:
        profile = request.user.profile
        return profile if (isinstance(profile, Profile)) else None
    except:
        return None

def index(request):
    current_profile = get_current_profile(request)
    profiles = None
    posts = None
    if current_profile:
        profiles = Profile.objects.all()
        posts = current_profile.get_timeline()
    return render(request, 'index.html', {"current_profile": current_profile, "profiles": profiles, "posts": posts})

@login_required
def show_profile(request, id):
    current_profile = get_current_profile(request)
    pfl = Profile.objects.get(id=id)
    if pfl.is_visible:
        return render(request, 'perfil.html', {
            "current_profile": current_profile,
            "is_friend": current_profile.is_friend_of(pfl),
            "has_invited": current_profile.has_invited(pfl),
            "is_blocked_by": current_profile.is_blocked_by(pfl),
            "has_blocked": current_profile.has_blocked(pfl),
            "profile": pfl,
        })
    else:
        return redirect('index')


@login_required
def view_convites(request):
    current_profile = get_current_profile(request)
    return render(request, 'convite.html', {
        "current_profile": current_profile,
        "convites": current_profile.convites_made.all(),
        "invited": current_profile.convites_received.all()
    })


@login_required
def invite_profile(request, id):
    invited_profile = Profile.objects.get(id=id)
    current_profile = get_current_profile(request)
    current_profile.invite(invited_profile)
    return redirect('view_convites')


@login_required
def invite_accept(request, invite_id):
    accepted_invite = Invite.objects.get(id=invite_id)
    accepted_invite.accept()
    return redirect('convites')


@login_required
def invite_decline(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    invite.delete()
    return redirect('convites')


@login_required
def view_friends(request):
    current_profile = get_current_profile(request)
    return render(request, 'friends.html', {
        "current_profile": current_profile,
        "friends": current_profile.friends.all()
    })


@login_required
def remove_a_friend(request, friend_id):
    current_profile = get_current_profile(request)
    friend_profile = Profile.objects.get(id=friend_id)
    current_profile.remove_friend(friend_profile)
    return redirect('friends')


@login_required
def block(request, id):
    current_profile = get_current_profile(request)
    pfl = Profile.objects.get(id=id)
    previous_page = 'friends' if ('friends' in request.META['HTTP_REFERER']) else 'show_profile'
    current_profile.block(pfl)
    return redirect(previous_page) if previous_page == 'friends' else redirect(previous_page, id=id)


@login_required
def blocks(request):
    current_profile = get_current_profile(request)
    return render(request, 'bloqueios.html', {
        "current_profile": current_profile,
        "blocks": current_profile.blocks_made.all()
    })


@login_required
def remove_block(request, id):
    current_profile = get_current_profile(request)
    pfl = Profile.objects.get(id=id)
    previous_page = 'blocks' if ('blocks' in request.META['HTTP_REFERER']) else 'show_profile'
    current_profile.remove_block(pfl)
    return redirect(previous_page) if previous_page == 'blocks' else redirect(previous_page, id=id)

@login_required
def toggle_superuser(request, id):
    current_profile = get_current_profile(request)
    pfl = Profile.objects.get(id=id)
    if current_profile.user.is_superuser:
        is_superuser = pfl.user.is_superuser
        pfl.user.is_superuser = not is_superuser
        print("%s is now superuser (%s)" % (pfl, pfl.user.is_superuser))
        pfl.user.save()
    return redirect('show_profile', id=id)


@login_required
def deactivate_profile(request, id):
    current_profile = get_current_profile(request)
    if current_profile is Profile and (current_profile.id == id or current_profile.user.is_superuser):
        pfl = Profile.objects.get(id=id)
        pfl.is_visible = False
        pfl.save()
        return redirect('logout')
    return redirect('index')


@login_required
def remove_profile(request, id):
    current_profile = get_current_profile(request)
    if current_profile is Profile and (current_profile.id == id or current_profile.user.is_superuser):
        pfl = Profile.objects.get(id=id)
        pfl.delete()
        return redirect('logout')
    return redirect('index')
