# Generated by Django 3.2 on 2022-04-09 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0020_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.TextField(default='0'),
            preserve_default=False,
        ),
    ]
