# Generated by Django 2.1.3 on 2019-01-29 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invest_app', '0004_auto_20190129_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invest',
            name='product_type',
        ),
    ]