# Generated by Django 5.0.1 on 2024-02-10 08:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0007_ordert'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ordert',
            new_name='Order',
        ),
    ]