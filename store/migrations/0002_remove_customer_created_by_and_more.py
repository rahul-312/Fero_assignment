# Generated by Django 5.1.2 on 2024-10-17 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='updated_by',
        ),
    ]