# Generated by Django 2.1.7 on 2019-03-02 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0004_merchant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdetail',
            options={'verbose_name': 'UserDetail', 'verbose_name_plural': 'UserDetails'},
        ),
    ]