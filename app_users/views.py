from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model


from .forms import UserRegistrationForm


User = get_user_model()


def user_registration(request):


    """
    View function to handle user registration.
    
        - Extracts registration data from the request.
        - Checks if the provided passwords match and if the username is available.
        - If conditions are met, creates a new user and redirects to the login page.
    
    """

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if password1 == password2 and not user:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                
            )
            user.set_password(password2)
            user.save()
            return redirect('login')


    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'app_users/registration.html', context)


def login_user(request):


    """
    View function to handle user login.

        - Extracts login credentials from the request.
        - Checks if the provided username exists and if the password is correct.
        - If the user exists and the password is correct, logs the user in and redirects to the home page.

    """
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user_exists = user.check_password(password)
        except:
            user_exists = None
            user = None

        if user_exists:
            login(request, user)
            return redirect('home')
    return render(request, 'app_users/login.html')


def logout_user(request):

    """
    View function to handle user logout.

    Logs out the currently authenticated user and redirects to the login page.

    """

    logout(request)
    return redirect('login') 