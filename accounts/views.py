from accounts.models import (
    AccountGroup,
    CompanyAccount,
    JournalVoucherAccount,
    SubAccount,
)
from accounts.serializers import (
    CreateJournalVoucherSerializer,
    CreateSalesConfirmationTransactionSerializer,
    GetCompanyAccountSerializer,
    GetJournalVoucherAccountSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .helpers import AccountHelpers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountCRDRViewSet(viewsets.ModelViewSet):
    queryset = JournalVoucherAccount.objects.all()
    serializer_class = GetJournalVoucherAccountSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        currency = request.data.get("currency_id")
        DR_accounty_type = request.data.get("account_type")

        account_group, _ = AccountGroup.objects.get_or_create(name=DR_accounty_type)

        sub_account, _ = SubAccount.objects.get_or_create(
            name=DR_accounty_type,
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
            "account": None,
        }

        jour_voucher_account_entity_data = {
            "journal_voucher_account": None,
            "accountable_id": request.data.get("accountable_id"),
            "accountable_type_id": request.data.get("accountable_type_id"),
        }

        # with transaction.atomic():  # Begin a transaction block

        # Creating Journal Voucher
        # First, create the journal voucher
        jour_voucher_serializer = CreateJournalVoucherSerializer(data=jour_voucher_data)
        if not jour_voucher_serializer.is_valid():
            return Response(
                {"error": jour_voucher_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        jour_voucher = jour_voucher_serializer.save()

        # Now attempt to create CR
        cr_response = AccountHelpers.create_CR(
            account_data=account_data,
            company_account_data=company_account_data,
            jour_voucher_account_data=jour_voucher_account_data,
            jour_voucher_account_entity_data=jour_voucher_account_entity_data,
            CR_accounty_type="SALES_ACCOUNT",
            jour_voucher=jour_voucher,
        )

        # If CR creation returned an error response
        if isinstance(cr_response, Response):
            # Optionally, you could also delete created journal_voucher if needed
            jour_voucher.delete()
            return cr_response  # Return the error response from create_CR

        # Now attempt to create DR
        dr_response = AccountHelpers.create_DR(
            account_data=account_data,
            company_account_data=company_account_data,
            jour_voucher_account_data=jour_voucher_account_data,
            jour_voucher_account_entity_data=jour_voucher_account_entity_data,
            DR_accounty_type=DR_accounty_type,
            jour_voucher=jour_voucher,
        )

        # If DR creation returned an error response
        if isinstance(dr_response, Response):
            # Clean up previously created journal_voucher, CR objects as necessary here
            # For instance, you might delete the previously created objects if needed
            jour_voucher.delete()
            # You may need to handle deletions of CR-related objects depending on their state
            return dr_response  # Return the error response from create_DR

        # Save sales confirmation transaction
        sales_transaction_data = {
            "journal_voucher": jour_voucher.id,
            "sales_confirmation_id": request.data.get("sales_confirmation_id"),
        }

        sales_transaction_serializer = CreateSalesConfirmationTransactionSerializer(
            data=sales_transaction_data
        )

        if not sales_transaction_serializer.is_valid():
            # Clean up created objects if necessary, similar to above

            jour_voucher.delete()
            JournalVoucherAccount.objects.filter(
                journal_voucher=jour_voucher.id
            ).delete()

            return Response(
                {"error": sales_transaction_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sales_transaction_serializer.save()  # Save sales confirmation transaction

        # Successfully created all items
        return Response(
            {
                "message": "Saved successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class AccountDRCRViewSet(viewsets.ModelViewSet):
    queryset = JournalVoucherAccount.objects.all()
    serializer_class = GetJournalVoucherAccountSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        currency = request.data.get("currency_id")
        CR_account_type = request.data.get("account_type")

        account_group, _ = AccountGroup.objects.get_or_create(name=CR_account_type)

        sub_account, _ = SubAccount.objects.get_or_create(
            name=CR_account_type,
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
            "account": None,
        }

        jour_voucher_account_entity_data = {
            "journal_voucher_account": None,
            "accountable_id": request.data.get("accountable_id"),
            "accountable_type_id": request.data.get("accountable_type_id"),
        }

        # with transaction.atomic():  # Begin a transaction block

        # Creating Journal Voucher
        # First, create the journal voucher
        jour_voucher_serializer = CreateJournalVoucherSerializer(data=jour_voucher_data)
        if not jour_voucher_serializer.is_valid():
            return Response(
                {"error": jour_voucher_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        jour_voucher = jour_voucher_serializer.save()

        # Now attempt to create DR
        dr_response = AccountHelpers.create_DR(
            account_data=account_data,
            company_account_data=company_account_data,
            jour_voucher_account_data=jour_voucher_account_data,
            jour_voucher_account_entity_data=jour_voucher_account_entity_data,
            DR_accounty_type="DEBTOR_ACCOUNT",
            jour_voucher=jour_voucher,
        )

        # If DR creation returned an error response
        if isinstance(dr_response, Response):
            # Optionally, you could also delete created journal_voucher if needed
            jour_voucher.delete()
            return dr_response  # Return the error response from create_DR

        # Now attempt to create CR
        cr_response = AccountHelpers.create_CR(
            account_data=account_data,
            company_account_data=company_account_data,
            jour_voucher_account_data=jour_voucher_account_data,
            jour_voucher_account_entity_data=jour_voucher_account_entity_data,
            CR_accounty_type=CR_account_type,
            jour_voucher=jour_voucher,
        )

        # If CR creation returned an error response
        if isinstance(cr_response, Response):
            # Clean up previously created journal_voucher, DR objects as necessary here
            # For instance, you might delete the previously created objects if needed
            jour_voucher.delete()
            # You may need to handle deletions of DR-related objects depending on their state
            return cr_response  # Return the error response from create_CR

        sales_transaction_data = {
            "journal_voucher": jour_voucher.id,
            "sales_confirmation_id": request.data.get("sales_confirmation_id"),
        }

        sales_transaction_serializer = CreateSalesConfirmationTransactionSerializer(
            data=sales_transaction_data
        )

        if not sales_transaction_serializer.is_valid():
            # Clean up created objects if necessary, similar to above

            jour_voucher.delete()
            JournalVoucherAccount.objects.filter(
                journal_voucher=jour_voucher.id
            ).delete()

            return Response(
                {"error": sales_transaction_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sales_transaction_serializer.save()  # Save sales confirmation transaction

        # Successfully created all items
        return Response(
            {
                "message": "Saved successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class CompanyAccountViewSet(viewsets.ModelViewSet):
    queryset = CompanyAccount.objects.all()
    serializer_class = GetCompanyAccountSerializer
    permission_classes = [IsAuthenticated]
