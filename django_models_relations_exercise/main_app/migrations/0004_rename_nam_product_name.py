# Generated by Django 5.0.4 on 2024-07-07 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_product_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='nam',
            new_name='name',
        ),
    ]