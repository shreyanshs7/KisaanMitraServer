# Generated by Django 2.1.7 on 2019-03-02 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advisory', '0003_auto_20190302_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='advice',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/uploads/advice_covers/'),
        ),
    ]
