# Generated by Django 5.0.3 on 2024-03-25 20:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_alter_comment_post'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date']},
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['date'], name='forum_comme_date_d7fe2c_idx'),
        ),
    ]