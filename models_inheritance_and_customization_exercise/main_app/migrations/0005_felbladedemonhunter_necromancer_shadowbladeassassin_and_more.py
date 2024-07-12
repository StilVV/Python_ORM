# Generated by Django 5.0.6 on 2024-07-09 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_timemage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FelbladeDemonHunter',
            fields=[
                ('demonhunter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.demonhunter')),
                ('felblade_ability', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.demonhunter',),
        ),
        migrations.CreateModel(
            name='Necromancer',
            fields=[
                ('mage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.mage')),
                ('raise_dead_ability', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.mage',),
        ),
        migrations.CreateModel(
            name='ShadowbladeAssassin',
            fields=[
                ('assassin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.assassin')),
                ('shadowstep_ability', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.assassin',),
        ),
        migrations.CreateModel(
            name='VengeanceDemonHunter',
            fields=[
                ('demonhunter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.demonhunter')),
                ('vengeance_mastery', models.CharField(max_length=100)),
                ('retribution_ability', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.demonhunter',),
        ),
        migrations.CreateModel(
            name='ViperAssassin',
            fields=[
                ('assassin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.assassin')),
                ('venomous_strikes_mastery', models.CharField(max_length=100)),
                ('venomous_bite_ability', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.assassin',),
        ),
    ]
