from django.shortcuts import render, redirect
from .models import Cost







def home_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    full_name = request.user.get_full_name()
    context = {
        "full_name": full_name,
    }

    return render(request, 'app_main/home.html', context)



def costs(request):
    if not request.user.is_authenticated:
        return redirect('login')

    costs_list = Cost.objects.filter(owner_id=request.user)

    context = {
        'costs': costs_list
    }

    return render(request, 'app_main/home.html', context)
