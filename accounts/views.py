from accounts.models import (
    Account,
    AccountGroup,
    Currency,
    JournalVoucherAccount,
    SubAccount,
)
from accounts.serializers import (
    CreateAccountSerializer,
    CreateJournalVoucherAccountEntitySerializer,
    CreateJournalVoucherAccountSerializer,
    CreateJournalVoucherSerializer,
    CreateSubAccountSerializer,
    GetAccountSerializer,
    GetJournalVoucherSerializer,
    GetSubAccountSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .helpers import AccountHelpers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = JournalVoucherAccount.objects.all()
    serializer_class = CreateJournalVoucherAccountSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        currency = request.data.get("currency_id")

        account_group, _ = AccountGroup.objects.get_or_create(
            name=request.data.get("account")
        )

        sub_account, _ = SubAccount.objects.get_or_create(
            name=request.data.get("account"),
            account_group=account_group,
        )
        # debtors
        account_data = {
            "sub_account": sub_account.id,
            "name": sub_account.name,
            "payment_type": "ONE_TIME",
        }

        jour_voucher_data = {
            "user": request.user.id,
            "currency": currency,
            "date": request.data.get("date"),
            "reference_number": request.data.get("reference_number"),
            "exchange_rate": request.data.get("exchange_rate"),
            "transaction_type": request.data.get("transaction_type"),
            "transaction_id": request.data.get("transaction_id"),
            "cheque_number": request.data.get("cheque_number"),
            "control_number": request.data.get("control_number"),
            "remarks": request.data.get("remarks"),
        }

        jour_voucher_account_data = {
            "journal_voucher": None,
            "account": None,
            "currency": currency,
            "amount": request.data.get("amount"),
            "transaction_type": None,
            "narration": request.data.get("narration"),
        }

        company_account_data = {
            "account_type": "DEBTOR_ACCOUNT",
            "account": None,
        }

        jour_voucher_account_entity_data = {
            "journal_voucher_account": None,
            "accountable_id": request.data.get("accountable_id"),
            "accountable_type_id": request.data.get("accountable_type_id"),
        }

        with transaction.atomic():  # Begin a transaction block
            try:
                cr_response = AccountHelpers.create_CR(
                    account_data=account_data,
                    company_account_data=company_account_data,
                    jour_voucher_data=jour_voucher_data,
                    jour_voucher_account_data=jour_voucher_account_data,
                    jour_voucher_account_entity_data=jour_voucher_account_entity_data,
                )

                # Check if CR creation returned an error response
                if isinstance(cr_response, Response):
                    return cr_response  # Return the error response from create_CR

                dr_response = AccountHelpers.create_DR(
                    account_data=account_data,
                    company_account_data=company_account_data,
                    jour_voucher_data=jour_voucher_data,
                    jour_voucher_account_data=jour_voucher_account_data,
                    jour_voucher_account_entity_data=jour_voucher_account_entity_data,
                )

                # Check if DR creation returned an error response
                if isinstance(dr_response, Response):
                    return dr_response  # Return the error response from create_DR

                return Response(
                    {"message": "Saved successfully"}, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
