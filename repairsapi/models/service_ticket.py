from django.db import models


class ServiceTicket(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name='submitted_tickets')
    employee = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_tickets')
    description = models.CharField(max_length=155)
    emergency = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)