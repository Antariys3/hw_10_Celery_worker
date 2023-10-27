from django.db import models


class PhoneNumberVerification(models.Model):
    phone_number = models.CharField(max_length=16)
    verification_code = models.CharField(max_length=6)
    attempts_counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.phone_number} - {self.verification_code}"
