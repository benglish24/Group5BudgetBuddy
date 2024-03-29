# Generated by Django 5.0.2 on 2024-03-05 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0002_userdashboard_delete_financialdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdashboard',
            name='fixed_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='userdashboard',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='userdashboard',
            name='saving_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='userdashboard',
            name='spending',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
