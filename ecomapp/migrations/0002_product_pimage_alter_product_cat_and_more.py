# Generated by Django 5.0.1 on 2024-02-07 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pimage',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Mobile'), (2, 'Shoes'), (3, 'Cloth')], verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdeatil',
            field=models.CharField(max_length=300, verbose_name='Product Detail'),
        ),
    ]