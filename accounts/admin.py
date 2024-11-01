from django.contrib import admin
from .models import (
    Account,
    AccountGroup,
    SubAccount,
    Currency,
    JournalVoucher,
    JournalVoucherAccount,
    JournalVoucherAccountEntity,
)

# Register your models here.

admin.site.register(Account)
admin.site.register(AccountGroup)
admin.site.register(SubAccount)
admin.site.register(Currency)
admin.site.register(JournalVoucher)
admin.site.register(JournalVoucherAccount)
admin.site.register(JournalVoucherAccountEntity)
