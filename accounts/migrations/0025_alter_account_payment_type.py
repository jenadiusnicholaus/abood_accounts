# Generated by Django 5.1.2 on 2024-11-04 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_journalvoucheraccountentity_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='payment_type',
            field=models.CharField(choices=[('ONE_TIME', 'One Time'), ('PERIODIC', 'Periodic')], default='ONE_TIME', max_length=20),
        ),
    ]
