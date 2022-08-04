from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CreateUserForm, Authenticate, CreatePlayer
from django.contrib.auth import authenticate, login
from .models import Player
from django.shortcuts import get_object_or_404


def account(request):
    if request.user.is_authenticated:
        player_id = request.user.id
        player = Player.objects.get(id=player_id)
        data = {
            'player': player
        }
        return render(request, 'account/account.html', data)
    else:
        return render(request, 'account/account.html')


def view_profile(request, username):
    player = get_object_or_404(Player, username=username)
    data = {
        'player': player
    }
    return render(request, 'account/profile.html', data)


@login_required(login_url='login')
def profile_settings(request, username):
    player = get_object_or_404(Player, username=username)
    data = {
        'player': player
    }
    return render(request, 'account/settings.html', data)


def register(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        error = ''
        form = CreateUserForm()

        if request.method == 'POST':
            forma = CreatePlayer(request.POST)
            if forma.is_valid():
                forma.save()
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('account_home')
            else:
                error = 'Неправильно введенные данные'

        data = {
            'form': form,
            'error': error
        }
        return render(request, 'registration/register.html', data)


def login_acc(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        error = ''
        form = Authenticate()
        if request.method == 'POST':
            form = Authenticate(data=request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            else:
                error = 'Неправильно введенные данные'

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'registration/login.html', data)
