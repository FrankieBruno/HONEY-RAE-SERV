from django.db import models


class Ticket(models.Model):
    """Service ticket for tech repairs"""

    # Priority choices
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_URGENT, 'Urgent'),
    ]

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name='submitted_tickets')
    employee = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_tickets')
    description = models.CharField(max_length=500)
    emergency = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['-date_created']

    @property
    def status(self):
        """Computed status based on employee assignment and completion"""
        if self.date_completed:
            return 'completed'
        elif self.employee:
            return 'in_progress'
        else:
            return 'open'

    def __str__(self):
        return f"Ticket #{self.id}: {self.description[:50]}"