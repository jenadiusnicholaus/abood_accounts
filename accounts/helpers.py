# import logging
from rest_framework.response import Response
from rest_framework import status

from accounts.models import AccountGroup
from accounts.serializers import (
    CreateAccountSerializer,
    CreateCompanyAccountSerializer,
    CreateJournalVoucherAccountEntitySerializer,
    CreateJournalVoucherAccountSerializer,
    CreateJournalVoucherSerializer,
)


class AccountHelpers:
    @staticmethod
    def create_CR(
        account_data,
        company_account_data,
        jour_voucher_account_data,
        jour_voucher_account_entity_data,
        CR_accounty_type,
        jour_voucher,
    ):
        saved_objects = {}

        try:
            saved_objects["account"] = AccountHelpers._create_account(account_data)
            if isinstance(saved_objects["account"], Response):
                return saved_objects["account"]  # Return Response if an error occurred

            saved_objects["company_account"] = AccountHelpers._create_company_account(
                company_account_data, saved_objects["account"].id, CR_accounty_type
            )
            if isinstance(saved_objects["company_account"], Response):
                return saved_objects[
                    "company_account"
                ]  # Return Response if an error occurred

            saved_objects["jour_voucher_account"] = (
                AccountHelpers._create_journal_voucher_account(
                    jour_voucher_account_data,
                    jour_voucher,
                    saved_objects["company_account"],
                )
            )
            if isinstance(saved_objects["jour_voucher_account"], Response):
                # Only delete the jour_voucher_account if it failed
                if saved_objects["jour_voucher_account"]:
                    saved_objects["jour_voucher_account"].delete()
                return saved_objects[
                    "jour_voucher_account"
                ]  # Return Response if an error occurred

            saved_objects["jour_voucher_account_entity"] = (
                AccountHelpers._create_journal_voucher_account_entity(
                    jour_voucher_account_entity_data,
                    saved_objects["jour_voucher_account"].id,
                )
            )
            if isinstance(saved_objects["jour_voucher_account_entity"], Response):
                if saved_objects["jour_voucher_account"]:
                    saved_objects["jour_voucher_account"].delete()  # Clean up if fails
                return saved_objects["jour_voucher_account_entity"]

            return saved_objects

        except Exception as e:
            # Rollback only the jour_voucher_account if an exception occurs
            if (
                "jour_voucher_account" in saved_objects
                and saved_objects["jour_voucher_account"]
            ):
                saved_objects["jour_voucher_account"].delete()

            return Response(
                {"error": f"An internal server error occurred. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def create_DR(
        account_data,
        company_account_data,
        jour_voucher_account_data,
        jour_voucher_account_entity_data,
        DR_accounty_type,
        jour_voucher,
    ):
        saved_objects = {}

        try:
            saved_objects["account"] = AccountHelpers._create_account(account_data)
            if isinstance(saved_objects["account"], Response):
                return saved_objects["account"]  # Return Response if an error occurred

            saved_objects["company_account"] = AccountHelpers._create_company_account(
                company_account_data, saved_objects["account"].id, DR_accounty_type
            )
            if isinstance(saved_objects["company_account"], Response):
                return saved_objects[
                    "company_account"
                ]  # Return Response if an error occurred

            saved_objects["jour_voucher_account"] = (
                AccountHelpers._create_journal_voucher_account(
                    jour_voucher_account_data,
                    jour_voucher,
                    saved_objects["company_account"],
                    transaction_type="DR",
                )
            )
            if isinstance(saved_objects["jour_voucher_account"], Response):
                # Only delete the jour_voucher_account if it failed
                if saved_objects["jour_voucher_account"]:
                    saved_objects["jour_voucher_account"].delete()
                return saved_objects[
                    "jour_voucher_account"
                ]  # Return Response if an error occurred

            saved_objects["jour_voucher_account_entity"] = (
                AccountHelpers._create_journal_voucher_account_entity(
                    jour_voucher_account_entity_data,
                    saved_objects["jour_voucher_account"].id,
                )
            )
            if isinstance(saved_objects["jour_voucher_account_entity"], Response):
                if saved_objects["jour_voucher_account"]:
                    saved_objects["jour_voucher_account"].delete()  # Clean up if fails
                return saved_objects["jour_voucher_account_entity"]

            return saved_objects

        except Exception as e:
            # Rollback only the jour_voucher_account if an exception occurs
            if (
                "jour_voucher_account" in saved_objects
                and saved_objects["jour_voucher_account"]
            ):
                saved_objects["jour_voucher_account"].delete()

            return Response(
                {"error": f"An internal server error occurred. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def _create_account(account_data):
        account_serializer = CreateAccountSerializer(data=account_data)
        if not account_serializer.is_valid():
            return Response(
                {"error": account_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return account_serializer.save()

    @staticmethod
    def _create_company_account(company_account_data, account_id, account_type):
        company_account_data["account"] = account_id
        company_account_data["account_type"] = account_type
        company_serializer = CreateCompanyAccountSerializer(data=company_account_data)
        if not company_serializer.is_valid():
            return Response(
                {"error": company_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return company_serializer.save()

    @staticmethod
    def _create_journal_voucher_account(
        journal_voucher_account_data,
        jour_voucher,
        company_account,
        transaction_type="CR",
    ):
        journal_voucher_account_data["journal_voucher"] = jour_voucher.id
        journal_voucher_account_data["account"] = company_account.id
        journal_voucher_account_data["transaction_type"] = transaction_type
        journal_voucher_account_serializer = CreateJournalVoucherAccountSerializer(
            data=journal_voucher_account_data
        )
        if not journal_voucher_account_serializer.is_valid():
            return Response(
                {"error": journal_voucher_account_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return journal_voucher_account_serializer.save()

    @staticmethod
    def _create_journal_voucher_account_entity(
        jour_voucher_account_entity_data, jour_voucher_account_id
    ):
        jour_voucher_account_entity_data["journal_voucher_account"] = (
            jour_voucher_account_id
        )
        jour_voucher_account_entity_serializer = (
            CreateJournalVoucherAccountEntitySerializer(
                data=jour_voucher_account_entity_data
            )
        )
        if not jour_voucher_account_entity_serializer.is_valid():
            return Response(
                {"error": jour_voucher_account_entity_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return jour_voucher_account_entity_serializer.save()
