# Generated by Django 3.2.5 on 2021-07-15 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='blogger',
        ),
    ]