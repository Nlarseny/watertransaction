from django.db import models
from django.utils import timezone

#example
class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"


class TransferVariables(models.Model):
    water_right = models.CharField(max_length=300)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return (self.water_right, self.price, self.amount, self.start_date, self.end_date)