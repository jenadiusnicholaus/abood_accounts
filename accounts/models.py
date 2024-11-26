from django.db import models
from django.utils import timezone
import random
import string
from django.contrib.auth.models import User

from utils.utilities import Utilities
from django.conf import settings


class AccountGroup(models.Model):
    NAMES_CHOICES = settings.ACCOUNT_GROUP_CHOICES
    name = models.CharField(max_length=50, choices=NAMES_CHOICES)
    code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "account_groups"

    def __str__(self):
        return self.name

    def generate_code(self):
        if not self.code:
            code = Utilities.generate_code(4)
            self.code = code
        else:
            pass

    def save(self, *args, **kwargs):
        self.generate_code()
        super(AccountGroup, self).save(*args, **kwargs)


class SubAccount(models.Model):

    account_group = models.ForeignKey(
        AccountGroup, on_delete=models.CASCADE, related_name="sub_accounts_groups_set"
    )
    name = models.CharField(
        max_length=100,
        choices=settings.SUB_ACCOUNT_NAMES_CHOICES,
    )
    is_defined = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "sub_accounts"


class Account(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ("ONE_TIME", "One Time"),
        ("PERIODIC", "Periodic"),
    ]

    sub_account = models.ForeignKey(
        SubAccount, on_delete=models.CASCADE, related_name="accounts_set"
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=11, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES, default="ONE_TIME"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "accounts"

    def __str__(self):
        return self.name

    def generate_code(self):
        if not self.code:
            code = Utilities.generate_code(4)
            self.code = code
        else:
            pass

    def save(self, *args, **kwargs):
        self.generate_code()
        super(Account, self).save(*args, **kwargs)


class CompanyAccount(models.Model):
    ACCOUNT_TYPE_CHOICES = settings.COMPADNY_ACCOUNT_TYPE_CHOICES
    account_type = models.CharField(
        max_length=50, choices=ACCOUNT_TYPE_CHOICES, default="SALES_ACCOUNT"
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="company_accounts_set",
        null=True,
    )

    class Meta:
        verbose_name_plural = "Company Accounts"
        db_table = "company_accounts"

    def __str__(self):
        return self.account_type


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Currencies"
        db_table = "currencies"

    def __str__(self):
        return self.name


class JournalVoucher(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("SALES_INVOICE", "Sales Invoice"),
        ("RECEIPT", "Receipt"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="currency_used_set", null=True
    )
    date = models.DateTimeField(null=True, blank=True)
    reference_number = models.CharField(
        max_length=100, default="NULL", blank=True, null=True
    )
    exchange_rate = models.FloatField(null=True, blank=True)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE_CHOICES, default="SALES_INVOICE"
    )
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    cheque_number = models.CharField(max_length=20, blank=True, null=True)
    control_number = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "journal_vouchers"


class JournalVoucherAccount(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("CR", "Credit"),
        ("DR", "Debit"),
    ]

    journal_voucher = models.ForeignKey(
        JournalVoucher, on_delete=models.CASCADE, related_name="accounts_set"
    )
    account = models.ForeignKey(
        CompanyAccount,
        on_delete=models.CASCADE,
        related_name="journal_voucher_accounts_set",
        null=True,
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True
    )
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPE_CHOICES)
    narration = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "journal_voucher_accounts"


class JournalVoucherAccountEntity(models.Model):
    journal_voucher_account = models.ForeignKey(
        JournalVoucherAccount,
        on_delete=models.CASCADE,
        related_name="entities_set",
        null=True,
    )
    accountable_id = models.BigIntegerField()
    accountable_type_id = models.BigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "journal_voucher_account_entities"
        unique_together = (("journal_voucher_account", "accountable_id"),)


class SalesConfirmationTransaction(models.Model):
    journal_voucher = models.ForeignKey(
        JournalVoucher,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_transactions_set",
    )
    sales_confirmation_id = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "sales_confirmation_transactions"
        unique_together = (("journal_voucher", "sales_confirmation_id"),)

    def __str__(self):
        return self.sales_confirmation_id
