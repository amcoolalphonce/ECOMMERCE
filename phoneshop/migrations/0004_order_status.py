# Generated by Django 4.0.5 on 2022-08-05 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phoneshop', '0003_alter_order_telephone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('sub', 'Received'), ('sta', 'Started'), ('comp', 'Completed')], default='sub', max_length=4),
        ),
    ]
