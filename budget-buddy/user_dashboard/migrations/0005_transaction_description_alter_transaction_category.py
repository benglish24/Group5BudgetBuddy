# Generated by Django 5.0.2 on 2024-03-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(default='MISCELLANEOUS', max_length=100),
        ),
    ]
