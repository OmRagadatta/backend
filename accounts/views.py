from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Profile
import uuid

# In-memory store of verification tokens (for simulation)
VERIFICATION_TOKENS = {}

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            image = form.cleaned_data.get('image')
            Profile.objects.create(user=user, image=image)
            token = str(uuid.uuid4())
            VERIFICATION_TOKENS[token] = user
            return redirect('accounts:verify', token=token)
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify(request, token):
    user = VERIFICATION_TOKENS.get(token)
    if user:
        user.is_active = True
        user.save()
        messages.success(request, "Account Verified Successfully ✅")
    else:
        messages.error(request, "Invalid Verification Link ❌")
    return redirect('accounts:login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, "Account not verified yet!")
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
