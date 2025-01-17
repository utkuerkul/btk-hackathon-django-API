# Generated by Django 5.1.2 on 2024-11-02 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_field_resultmodel_lessons_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useractivitysuggestion',
            old_name='long_term_goals',
            new_name='goals',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='concentration_duration',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='height',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='preferred_resources',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='review_notes',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='short_term_goals',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='stress_level',
        ),
        migrations.RemoveField(
            model_name='useractivitysuggestion',
            name='weight',
        ),
    ]
