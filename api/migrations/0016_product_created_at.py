# Generated by Django 5.1.7 on 2025-03-31 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_order_product_alter_product_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='exit'),
            preserve_default=False,
        ),
    ]
