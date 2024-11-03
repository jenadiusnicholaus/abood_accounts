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
        jour_voucher_data,
        jour_voucher_account_data,
        jour_voucher_account_entity_data,
    ):
        sub_account = None
        account = None
        jour_voucher = None
        company_account = None
        jour_voucher_account = None

        try:
            # Create or get the account group

            # Creating Sub Account
            # sub_account_serializer = CreateSubAccountSerializer(data=sub_account_data)
            # if not sub_account_serializer.is_valid():
            #     return Response(
            #         {"error": sub_account_serializer.errors},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            # sub_account = sub_account_serializer.save()

            # Creating Account
            # account_data["sub_account"] = sub_account.id
            account_serializer = CreateAccountSerializer(data=account_data)
            if not account_serializer.is_valid():
                sub_account.delete()  # Clean up on error
                return Response(
                    {"error": account_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            account = account_serializer.save()

            # Creating Journal Voucher
            jour_voucher_serializer = CreateJournalVoucherSerializer(
                data=jour_voucher_data
            )
            if not jour_voucher_serializer.is_valid():
                account.delete()  # Clean up on error
                sub_account.delete()
                return Response(
                    {"error": jour_voucher_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            jour_voucher = jour_voucher_serializer.save()

            # Creating Company Account
            company_account_data["account"] = account.id
            company_serializers = CreateCompanyAccountSerializer(
                data=company_account_data
            )
            if not company_serializers.is_valid():
                jour_voucher.delete()  # Clean up on error
                account.delete()
                # sub_account.delete()
                return Response(
                    {"error": company_serializers.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            company_account = company_serializers.save()

            # Creating Journal Voucher Account
            jour_voucher_account_data["journal_voucher"] = jour_voucher.id
            jour_voucher_account_data["account"] = company_account.id
            jour_voucher_account_data["transaction_type"] = "CR"
            jour_voucher_account_serializer = CreateJournalVoucherAccountSerializer(
                data=jour_voucher_account_data
            )
            if not jour_voucher_account_serializer.is_valid():
                company_account.delete()  # Clean up on error
                jour_voucher.delete()
                account.delete()
                return Response(
                    {"error": jour_voucher_account_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            jour_voucher_account = jour_voucher_account_serializer.save()

            # Creating Journal Voucher Account Entity
            jour_voucher_account_entity_data["journal_voucher_account"] = (
                jour_voucher_account.id
            )
            jour_voucher_account_entity_serializer = (
                CreateJournalVoucherAccountEntitySerializer(
                    data=jour_voucher_account_entity_data
                )
            )
            if not jour_voucher_account_entity_serializer.is_valid():
                jour_voucher_account.delete()  # Clean up on error
                company_account.delete()
                jour_voucher.delete()
                account.delete()
                # sub_account.delete()
                return Response(
                    {"error": jour_voucher_account_entity_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            jour_voucher_account_entity = jour_voucher_account_entity_serializer.save()

        except Exception as e:
            # logger.error(f"An error occurred during CR creation: {str(e)}")
            return Response(
                {"error": f"An internal server error occurred.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def create_DR(
        account_data,
        company_account_data,
        jour_voucher_data,
        jour_voucher_account_data,
        jour_voucher_account_entity_data,
    ):
        sub_account = None
        account = None
        jour_voucher = None
        company_account = None
        jour_voucher_account = None

        try:
            # Similar logic to create_CR with appropriate adjustments
            # Creating Sub Account
            # sub_account_serializer = CreateSubAccountSerializer(data=sub_account_data)
            # if not sub_account_serializer.is_valid():
            #     return Response(
            #         {"error": sub_account_serializer.errors},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            # sub_account = sub_account_serializer.save()

            # Creating Account
            # account_data["sub_account"] = sub_account.id
            account_serializer = CreateAccountSerializer(data=account_data)
            if not account_serializer.is_valid():
                sub_account.delete()
                return Response(
                    {"error": account_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            account = account_serializer.save()

            # Creating Journal Voucher
            jour_voucher_serializer = CreateJournalVoucherSerializer(
                data=jour_voucher_data
            )
            if not jour_voucher_serializer.is_valid():
                account.delete()
                # sub_account.delete()
                return Response(
                    {"error": jour_voucher_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            jour_voucher = jour_voucher_serializer.save()

            # Creating Company Account
            company_account_data["account"] = account.id
            company_serializers = CreateCompanyAccountSerializer(
                data=company_account_data
            )
            if not company_serializers.is_valid():
                jour_voucher.delete()
                account.delete()
                # sub_account.delete()
                return Response(
                    {"error": company_serializers.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            company_account = company_serializers.save()

            # Creating Journal Voucher Account
            jour_voucher_account_data["journal_voucher"] = jour_voucher.id
            jour_voucher_account_data["account"] = account.id
            jour_voucher_account_data["transaction_type"] = "DR"
            jour_voucher_account_serializer = CreateJournalVoucherAccountSerializer(
                data=jour_voucher_account_data
            )
            if not jour_voucher_account_serializer.is_valid():
                company_account.delete()
                jour_voucher.delete()
                account.delete()
                # sub_account.delete()
                return Response(
                    {"error": jour_voucher_account_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            jour_voucher_account = jour_voucher_account_serializer.save()

            # Creating Journal Voucher Account Entity
            jour_voucher_account_entity_data["journal_voucher_account"] = (
                jour_voucher_account.id
            )
            jour_voucher_account_entity_serializer = (
                CreateJournalVoucherAccountEntitySerializer(
                    data=jour_voucher_account_entity_data
                )
            )
            if not jour_voucher_account_entity_serializer.is_valid():
                jour_voucher_account.delete()
                company_account.delete()
                jour_voucher.delete()
                account.delete()
                # sub_account.delete()
                return Response(
                    {"error": jour_voucher_account_entity_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            jour_voucher_account_entity = jour_voucher_account_entity_serializer.save()

        except Exception as e:
            return Response(
                {"error": f"An internal server error occurred. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
