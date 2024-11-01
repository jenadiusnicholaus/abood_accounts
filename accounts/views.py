from accounts.models import Account, AccountGroup, Currency, JournalVoucherAccount
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = JournalVoucherAccount.objects.all()
    serializer_class = CreateJournalVoucherAccountSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        currency = request.data.get("currency")

        print(request.data)

        currency_obj, _ = Currency.objects.get_or_create(name=currency)

        account_group, _ = AccountGroup.objects.get_or_create(name="TRADE_DEBTORS")

        sub_account_data = {"account_group": account_group.id, "name": "TRADE_DEBTORS"}
        account_data = {
            "sub_account": None,
            "name": "Trade Debtors",
            "payment_type": request.data.get("payment_type"),
        }

        jour_voucher_data = {
            "user": request.user.id,
            "currency": currency_obj.id,
            "date": request.data.get("date"),
            "reference_number": request.data.get("reference_number"),
            "exchange_rate": request.data.get("exchange_rate"),
            "transaction_type": request.data.get("transaction_mode"),
            "transaction_id": request.data.get("transaction_id"),
            "cheque_number": request.data.get("cheque_number"),
            "control_number": request.data.get("control_number"),
            "remarks": request.data.get("remarks"),
        }

        jour_voucher_account_data = {
            "journal_voucher": None,
            "account": None,
            "currency": currency_obj.id,
            "amount": request.data.get("amount"),
            "transaction_type": request.data.get("transaction_type"),
            "narration": request.data.get("narration"),
        }

        jour_voucher_account_entity_data = {
            "journal_voucher_account": None,
            "accountable_id": request.data.get("accountable_id"),
            "accountable_type_id": request.data.get("accountable_type_id"),
        }

        with transaction.atomic():
            sub_account_serializer = CreateSubAccountSerializer(data=sub_account_data)
            if not sub_account_serializer.is_valid():
                return Response(
                    sub_account_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            sub_account = sub_account_serializer.save()

            account_data["sub_account"] = sub_account.id
            account_serializer = CreateAccountSerializer(data=account_data)
            if not account_serializer.is_valid():
                # print(account_serializer.errors)
                sub_account.delete()
                return Response(
                    account_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            account = account_serializer.save()

            jour_voucher_serializer = CreateJournalVoucherSerializer(
                data=jour_voucher_data
            )
            if not jour_voucher_serializer.is_valid():
                print(jour_voucher_serializer.errors)
                sub_account.delete()
                account.delete()
                return Response(
                    jour_voucher_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            jour_voucher = jour_voucher_serializer.save()

            jour_voucher_account_data["journal_voucher"] = jour_voucher.id
            jour_voucher_account_data["account"] = account.id
            jour_voucher_account_serializer = CreateJournalVoucherAccountSerializer(
                data=jour_voucher_account_data
            )

            if not jour_voucher_account_serializer.is_valid():
                # print(jour_voucher_account_serializer.errors)
                sub_account.delete()
                account.delete()
                jour_voucher.delete()
                return Response(
                    jour_voucher_account_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            jour_voucher_account = jour_voucher_account_serializer.save()
            jour_voucher_account_entity_data["journal_voucher_account"] = (
                jour_voucher_account.id
            )
            jour_voucher_account_entity_serializer = (
                CreateJournalVoucherAccountEntitySerializer(
                    data=jour_voucher_account_entity_data
                )
            )

            if not jour_voucher_account_entity_serializer.is_valid():
                # print(jour_voucher_account_entity_serializer.errors)
                sub_account.delete()
                account.delete()
                jour_voucher.delete()
                jour_voucher_account.delete()
                return Response(
                    jour_voucher_account_entity_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            jour_voucher_account_entity = jour_voucher_account_entity_serializer.save()

        return Response(
            {"message": "Saved successfully"}, status=status.HTTP_201_CREATED
        )
