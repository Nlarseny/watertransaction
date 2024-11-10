from django.db import models
from django.utils import timezone

# example
class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"


class TransferVariables(models.Model):
    # user_id = models.CharField(max_length=200)
    # water_right = models.CharField(max_length=300)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    start_date = models.CharField(max_length=300)
    end_date = models.CharField(max_length=300)

    def __str__(self):
        """Returns a string representation of a message."""
        string_message = f"{self.price}&{self.amount}&{self.start_date}&{self.end_date}"
        return string_message