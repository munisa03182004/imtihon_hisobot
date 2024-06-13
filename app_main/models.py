
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cost(models.Model):
    """
    Model to represent a cost entry.

    This model represents an entry for a cost made by a user. It includes fields for the name of the cost,
    the amount, the payment type (e.g., 'Karta', 'Naqd'), the transaction type (e.g., 'Kirim', 'Chiqim'),
    the owner of the cost, and the date and time the cost was created.

    Attributes:
        TRANSACTION_TYPES (tuple): Choices for the transaction type field.
        PAYMENT_TYPES (tuple): Choices for the payment type field.
        owner_id (ForeignKey): The owner of the cost (a foreign key to the User model).
        name (CharField): The name of the cost.
        amount (DecimalField): The amount of the cost.
        payment_type (CharField): The payment type of the cost (choices from PAYMENT_TYPES).
        transaction_type (CharField): The transaction type of the cost (choices from TRANSACTION_TYPES).
        created (DateTimeField): The date and time the cost was created.
    """

    TRANSACTION_TYPES = (
        ('Kirim', 'Kirim'),
        ('Chiqim', 'Chiqim'),
    )
    PAYMENT_TYPES = (
        ('Karta', 'Karta'),
        ('Naqd', 'Naqd'),
    )

    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Default Name')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, default="Naqd")  
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

