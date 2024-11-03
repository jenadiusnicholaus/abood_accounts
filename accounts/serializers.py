# Serializers define the API representation.
from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import (
    Account,
    AccountGroup,
    CompanyAccount,
    Currency,
    JournalVoucher,
    JournalVoucherAccount,
    JournalVoucherAccountEntity,
    SubAccount,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# -------------------------- Account Group Serializers ----------


class GetAccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = "__all__"


class CreateAccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = "__all__"


class UpdateAccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = "__all__"


class GetSubAccountSerializer(serializers.ModelSerializer):
    account_group = GetAccountGroupSerializer(read_only=True)

    class Meta:
        model = SubAccount
        fields = "__all__"


class CreateSubAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAccount
        fields = "__all__"


class UpdateSubAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAccount
        fields = "__all__"


# ------- Account-------


class GetAccountSerializer(serializers.ModelSerializer):
    sub_account = GetSubAccountSerializer(read_only=True)

    class Meta:
        model = Account
        fields = "__all__"


class CreateAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"


class UpdateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


# ---------- Currency Serializers ----------


class GetCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CreateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class UpdateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


# -------------------------- JournalVoucher ----------


class GetJournalVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucher
        fields = "__all__"


class CreateJournalVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucher
        fields = "__all__"


class UpdateJournalVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucher
        fields = "__all__"


# ---------------JournalVoucherAccount----------------


class GetJournalVoucherAccountSerializer(serializers.Serializer):
    journal_voucher = GetJournalVoucherSerializer()
    account = GetAccountSerializer()
    entity = serializers.SerializerMethodField()
    currency = GetCurrencySerializer()

    def get_entity(self, obj):
        try:
            entity = JournalVoucherAccountEntity.objects.get(
                journal_voucher_account__id=obj.id
            )
            serializer = GetJournalVoucherAccountEntitySerializer(entity)
            return serializer.data

        except:
            return None

    class Meta:
        model = JournalVoucherAccount
        fields = "__all__"


class CreateJournalVoucherAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = JournalVoucherAccount
        fields = "__all__"


class UpdateJournalVoucherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucherAccount
        fields = "__all__"


# ----------JournalVoucherAccountEntitySerializer----------


class GetJournalVoucherAccountEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucherAccountEntity
        fields = "__all__"


class CreateJournalVoucherAccountEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucherAccountEntity
        fields = "__all__"


class UpdateJournalVoucherAccountEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucherAccountEntity
        fields = "__all__"


# ---------- Company Account Serializers ----------
class GetCompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAccount
        fields = "__all__"


class CreateCompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAccount
        fields = "__all__"


class UpdateCompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAccount
        fields = "__all__"
