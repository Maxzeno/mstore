# Generated by Django 4.1.7 on 2023-03-20 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_order_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='id',
        ),
    ]
