# Generated by Django 5.0.4 on 2024-08-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='status',
            field=models.CharField(choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Planned', max_length=9),
        ),
    ]
