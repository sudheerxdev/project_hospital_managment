from decimal import Decimal
from django.db import models
from apps.appointments.models import Appointment


class Bill(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ISSUED = "issued", "Issued"
        PAID = "paid", "Paid"

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="bill")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    generated_at = models.DateTimeField(auto_now_add=True)

    def recalculate(self):
        subtotal = sum(item.amount for item in self.items.all())
        self.subtotal = subtotal
        self.tax = (Decimal(subtotal) * Decimal("0.05")).quantize(Decimal("0.01"))
        self.total = (Decimal(self.subtotal) + Decimal(self.tax)).quantize(Decimal("0.01"))
        self.save(update_fields=["subtotal", "tax", "total"])


class BillLineItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.amount = (Decimal(self.quantity) * Decimal(self.unit_price)).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
