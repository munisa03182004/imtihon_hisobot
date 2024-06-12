from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        username (str): The unique username for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        date_joined (datetime): The date and time when the user joined.
        is_active (bool): Indicates if the user account is active.
        is_staff (bool): Indicates if the user is a staff member.
        is_superuser (bool): Indicates if the user has superuser permissions.
        groups (ManyToManyField): The groups to which the user belongs.
        user_permissions (ManyToManyField): The permissions granted to the user.

    Methods:
        __str__(): Returns the username of the user.
    """
    
    def __str__(self):
        return self.username
