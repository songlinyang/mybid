# Generated by Django 2.1.3 on 2019-01-29 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='invest',
            name='order_status',
            field=models.BooleanField(default=False, verbose_name='锁定状态'),
        ),
    ]
