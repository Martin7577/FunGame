# Generated by Django 5.0.3 on 2024-03-25 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='date_time',
            new_name='date',
        ),
    ]
