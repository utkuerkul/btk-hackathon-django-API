# Generated by Django 5.1.2 on 2024-11-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_yksexamresult'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yksexamresult',
            old_name='kontenjan_0',
            new_name='kontenjan',
        ),
        migrations.RenameField(
            model_name='yksexamresult',
            old_name='max_score_0',
            new_name='max_score',
        ),
        migrations.RenameField(
            model_name='yksexamresult',
            old_name='min_score_0',
            new_name='min_score',
        ),
        migrations.RenameField(
            model_name='yksexamresult',
            old_name='yerlesen_0',
            new_name='yerlesen',
        ),
        migrations.AddField(
            model_name='yksexamresult',
            name='year',
            field=models.IntegerField(default='1'),
            preserve_default=False,
        ),
    ]
