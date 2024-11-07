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
    SalesConfirmationTransaction,
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

    def create(self, validated_data):
        sub_account = validated_data.get("sub_account")
        name = validated_data.get("name")
        payment_type = validated_data.get("payment_type")
        account, created = Account.objects.get_or_create(
            payment_type=payment_type,
            defaults={
                "sub_account": sub_account,
                "name": name,
            },
        )
        return account


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

    # def create(self, validated_data):
    #     # Assuming 'transaction_type' is a unique identifier for your application
    #     transaction_type = validated_data.get("transaction_type")

    #     # Get or create the journal voucher based on transaction_type
    #     journal_voucher, created = JournalVoucher.objects.create(
    #         transaction_type=transaction_type,
    #         defaults=validated_data,  # Set other fields only if creating a new instance
    #     )

    #     return journal_voucher


class UpdateJournalVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucher
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

    def create(self, validated_data):
        account = validated_data.get("account")
        account_type = validated_data.get("account_type")
        company_account, created = CompanyAccount.objects.get_or_create(
            account_type=account_type,
            defaults={
                "account": account,
            },
        )
        return company_account


class UpdateCompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAccount
        fields = "__all__"


# ---------------JournalVoucherAccount----------------


class GetJournalVoucherAccountSerializer(serializers.ModelSerializer):
    journal_voucher = GetJournalVoucherSerializer()
    account = GetCompanyAccountSerializer()
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

    def create(self, validated_data):
        journal_voucher_account = validated_data.get("journal_voucher_account")
        accountable_id = validated_data.get("accountable_id")
        accountable_type_id = validated_data.get("accountable_type_id")
        entity, created = JournalVoucherAccountEntity.objects.get_or_create(
            accountable_id=accountable_id,
            journal_voucher_account=journal_voucher_account,
            defaults={
                "accountable_type_id": accountable_type_id,
            },
        )
        return entity


class UpdateJournalVoucherAccountEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucherAccountEntity
        fields = "__all__"


class GetSalesConfirmationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationTransaction
        fields = "__all__"


class CreateSalesConfirmationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = SalesConfirmationTransaction


class UpdateSalesConfirmationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationTransaction
        fields = "__all__"
