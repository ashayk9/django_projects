# Generated by Django 2.2.7 on 2020-02-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200228_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-detail'),
            preserve_default=False,
        ),
    ]
