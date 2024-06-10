from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Cost(models.Model):
    TRANSACTION_TYPES = (
        ('Kirim', 'Kirim'),
        ('Chiqim', 'Chiqim'),
    )

    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Default Name')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
