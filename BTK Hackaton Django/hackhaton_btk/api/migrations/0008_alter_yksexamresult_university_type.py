# Generated by Django 5.1.2 on 2024-11-07 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_yksexamresult_kontenjan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yksexamresult',
            name='university_type',
            field=models.CharField(max_length=100, verbose_name='Üniversites Türü'),
        ),
    ]
