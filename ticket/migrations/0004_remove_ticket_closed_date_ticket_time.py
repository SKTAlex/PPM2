# Generated by Django 5.0.6 on 2024-06-20 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_remove_ticket_description_ticket_is_purchased_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='closed_date',
        ),
        migrations.AddField(
            model_name='ticket',
            name='time',
            field=models.TimeField(default='00:00'),
        ),
    ]
