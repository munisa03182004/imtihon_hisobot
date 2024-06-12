# Generated by Django 5.0.6 on 2024-06-11 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0002_cost_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='payment_type',
            field=models.CharField(choices=[('Karta', 'Karta'), ('Naqd', 'Naqd')], default='Naqd', max_length=10),
        ),
    ]