from django.db import models
import uuid
from vms.models import Vendor


class PurchaseOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['po_number']),
            models.Index(fields=['vendor'])
        ]

    def __str__(self):
        return self.vendor.name + self.po_number

