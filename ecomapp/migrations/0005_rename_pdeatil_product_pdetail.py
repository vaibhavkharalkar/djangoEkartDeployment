# Generated by Django 5.0.1 on 2024-02-08 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0004_alter_cart_pid_alter_cart_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='pdeatil',
            new_name='pdetail',
        ),
    ]
