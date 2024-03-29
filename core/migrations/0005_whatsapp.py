# Generated by Django 4.0.6 on 2023-04-21 03:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_notification_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Whatsapp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=32)),
                ('token', models.CharField(max_length=1024)),
                ('template', models.CharField(max_length=128)),
            ],
        ),
    ]
