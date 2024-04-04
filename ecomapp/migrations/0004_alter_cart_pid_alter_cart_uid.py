# Generated by Django 5.0.1 on 2024-02-08 09:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_alter_product_pimage_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='pid',
            field=models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='ecomapp.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='uid',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
