# Generated by Django 5.1.2 on 2024-11-02 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_long_term_goals_useractivitysuggestion_goals_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='sleep_hours',
        ),
    ]
