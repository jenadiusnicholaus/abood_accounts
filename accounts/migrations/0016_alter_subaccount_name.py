# Generated by Django 5.1.2 on 2024-11-02 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_journalvoucher_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subaccount',
            name='name',
            field=models.CharField(choices=[('CASH_IN_HAND', 'CASH IN HAND'), ('BANK', 'BANK'), ('TRADE_DEBTORS', 'TRADE DEBTORS'), ('TRADE_CREDITORS', 'TRADE CREDITORS'), ('DIRECT_EXPENSES', 'DIRECT EXPENSES'), ('INDIRECT_EXPENSES', 'INDIRECT EXPENSES'), ('INVENTORY', 'INVENTORY'), ('MAINTENANCE_EXPENSES_HUNTING_VEHICLES', 'MAINTENANCE EXPENSES, HUNTING VEHICLES'), ('INCOME_TAX', 'INCOME TAX'), ('ACCOUNTS_RECEIVABLES', 'ACCOUNTS RECEIVABLES'), ('PREPAID_EXPENSES', 'PREPAID EXPENSES'), ('MAINTENANCE_EXPENSES_OTHER_VEHICLES_EQUIPMENT', 'MAINTENANCE EXPENSES, OTHER VEHICLES & EQUIPMENT'), ('PAYROLL_EXPENSES', 'PAYROLL EXPENSES'), ('ADMINISTRATIVE_EXPENSES', 'ADMINISTRATIVE EXPENSES'), ('ACCOUNTS_PAYABLE', 'ACCOUNTS PAYABLE')], max_length=100),
        ),
    ]
