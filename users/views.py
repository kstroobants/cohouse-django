from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileRegisterForm, ProfileUpdateForm


def create_profile(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileUpdateForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_create.html', context)


@login_required
def show_profile(request, pk):
    request_user = get_object_or_404(User, pk=pk)
    profile = request_user.profile
    context = {'request_user': request_user, 'profile': profile}
    return render(request, 'users/profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Account updated for {request.user.username}")
            return redirect('user-profile', pk=request.user.pk)
        else:
            for error in list(user_form.errors.values()):
                messages.error(request, error)
            for error in list(profile_form.errors.values()):
                messages.error(request, error)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_update.html', context)


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = SetPasswordForm(user)
    return render(request, 'users/password_change.html', {'form': form})

