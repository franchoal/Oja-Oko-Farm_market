# Generated by Django 5.1.7 on 2025-03-29 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_product_farmer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='farmer',
            new_name='user_id',
        ),
    ]
