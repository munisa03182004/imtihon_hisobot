from django.urls import path


from . import views

urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
