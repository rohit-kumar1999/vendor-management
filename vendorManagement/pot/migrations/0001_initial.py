# Generated by Django 4.2.8 on 2023-12-16 05:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('po_number', models.CharField(max_length=255, unique=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField()),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(max_length=255)),
                ('quality_rating', models.FloatField(null=True)),
                ('issue_date', models.DateTimeField()),
                ('acknowledgment_date', models.DateTimeField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vms.vendor')),
            ],
            options={
                'indexes': [models.Index(fields=['id'], name='pot_purchas_id_464e0f_idx'), models.Index(fields=['po_number'], name='pot_purchas_po_numb_6837e8_idx'), models.Index(fields=['vendor'], name='pot_purchas_vendor__a628e8_idx')],
            },
        ),
    ]
