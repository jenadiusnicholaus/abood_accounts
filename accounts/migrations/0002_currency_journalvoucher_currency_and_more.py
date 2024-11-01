# Generated by Django 5.1.2 on 2024-10-31 13:07

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'db_table': 'currencies',
            },
        ),
        migrations.AddField(
            model_name='journalvoucher',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='currency_used_set', to='accounts.currency'),
        ),
        migrations.AddField(
            model_name='journalvoucheraccount',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.currency'),
        ),
    ]
