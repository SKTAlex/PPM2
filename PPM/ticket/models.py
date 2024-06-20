import uuid
from django.db import models
from users.models import User


class Ticket(models.Model):
    ticket_number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField()
    time = models.TimeField(default='00:00')
    location = models.CharField(max_length=100, default='Da Definire')
    quantity_available = models.PositiveIntegerField(default=0)
    is_purchased = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_created_by')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    status_choices = (
        ('completed', 'completed'),
        ('pending', 'pending'),
        ('accepted', 'accepted')
    )
    ticket_status = models.CharField(max_length=20, choices=status_choices)

    def __str__(self):
        return self.title


class TicketPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField()
