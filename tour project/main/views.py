from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def welcome(request):
    return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        full_name = (request.POST.get('full_name') or '').strip()
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''

        if not all([full_name, username, email, password]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name.split()[0] if full_name.split() else '',
            last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else '',
        )
        user.save()
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page_html')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'home-page.html')


def home_page_html(request):
    guest_mode = not request.user.is_authenticated
    return render(request, 'home-page.html', {'guest_mode': guest_mode})


def explore_page(request):
    return render(request, 'explore.html', {'guest_mode': False})


def guest_home(request):
    return render(request, 'home-page.html', {'guest_mode': True})


def travel_plan(request):
    return render(request, 'travel_plan.html')


def events_page(request):
    return render(request, 'events.html')


def logout_view(request):
    logout(request)
    return redirect('login')
