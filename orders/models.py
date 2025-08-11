from django.db import models
from django.contrib.auth.models import User
from flowers.models import Flower

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.flower and self.quantity:
            self.total_price = self.flower.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
