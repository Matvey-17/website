from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.forms import UserFormLogin, UserRegisterForm, UserProfileForm
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserFormLogin(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'Вы успешно авторизовались!')
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserFormLogin()
    context = {
        'title': 'Store - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Store - Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required(login_url='users:login')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    total_sum = 0
    price_sum = 0
    for total in Basket.objects.filter(user=request.user):
        total_sum += total.quantity
        price_sum += total.quantity * total.product.price
    context = {
        'title': 'Store - Профиль',
        'form': form,
        'basket': Basket.objects.filter(user=request.user),
        'total_sum': total_sum,
        'price_sum': price_sum
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')
