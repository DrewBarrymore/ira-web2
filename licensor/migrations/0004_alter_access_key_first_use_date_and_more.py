# Generated by Django 4.1.7 on 2023-03-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licensor', '0003_alter_access_key_first_use_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_key',
            name='first_use_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='access_key',
            name='user_macid',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
