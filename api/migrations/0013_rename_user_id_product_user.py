# Generated by Django 5.1.7 on 2025-03-29 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_rename_user_product_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user_id',
            new_name='user',
        ),
    ]
