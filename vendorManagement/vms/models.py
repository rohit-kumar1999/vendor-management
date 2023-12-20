from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = PhoneNumberField()
    address = models.TextField()
    code = models.CharField(unique=True, max_length=255)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return self.name + "_" + self.code


class Performance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['vendor'])
        ]

    def __str__(self):
        return self.vendor.name + self.date
