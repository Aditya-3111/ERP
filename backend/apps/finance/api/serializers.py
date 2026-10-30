from rest_framework import serializers
from django.db import transaction
from apps.finance.models import AccountGroup, Ledger, Voucher, AccountingEntry, VoucherType


class VoucherTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherType
        fields = ['guid', 'name', 'parent', 'numbering_method', 'is_deemed_positive', 'affects_stock']
        read_only_fields = ['guid']


class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = ['guid', 'name', 'parent', 'primary_group', 'is_revenue',
                  'is_deemed_positive', 'affects_gross_profit', 'sort_position']
        read_only_fields = ['guid']


class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        # NOTE: file fields (gst_certificate, business_card, pan_card) are
        # intentionally left out - they need multipart upload, not JSON.
        fields = ['guid', 'name', 'parent', 'alias', 'description', 'notes',
                  'is_revenue', 'is_deemed_positive', 'opening_balance',
                  'opening_balance_type', 'closing_balance', 'mailing_name',
                  'address', 'city', 'state', 'country', 'pincode',
                  'contact_person', 'email', 'mobile', 'phone', 'website',
                  # tax / bank / credit details (were silently dropped before)
                  'pan', 'gstin', 'gst_registration_type', 'gst_supply_type',
                  'gst_duty_head', 'msme_no',
                  'bank_account_holder', 'bank_account_number', 'bank_ifsc',
                  'bank_swift', 'bank_name', 'bank_branch',
                  'bill_credit_period', 'credit_limit', 'is_active']
        read_only_fields = ['guid', 'closing_balance']


class AccountingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingEntry
        fields = ['guid', 'voucher', 'ledger', 'amount', 'amount_forex',
                  'currency', 'is_dr', 'narration']
        read_only_fields = ['guid']


class VoucherEntrySerializer(serializers.ModelSerializer):
    """Entry as nested inside a voucher (voucher is implied)."""

    class Meta:
        model = AccountingEntry
        fields = ['guid', 'ledger', 'amount', 'amount_forex', 'currency', 'is_dr', 'narration']


def next_voucher_number(voucher_type):
    """Auto number like SAL/0001 based on the voucher type name."""
    prefix = ''.join(w[0] for w in (voucher_type or 'VCH').split()).upper()
    if len(prefix) < 2:
        prefix = (voucher_type or 'VCH')[:3].upper()
    count = Voucher.objects.filter(voucher_type=voucher_type).count() + 1
    number = f"{prefix}/{count:04d}"
    while Voucher.objects.filter(voucher_type=voucher_type, voucher_number=number).exists():
        count += 1
        number = f"{prefix}/{count:04d}"
    return number


class VoucherSerializer(serializers.ModelSerializer):
    # The model's reverse relation is `accounting_entries`; the API (and both
    # frontends) call it `items`. Before this fix `items` was silently skipped.
    items = VoucherEntrySerializer(source='accounting_entries', many=True, required=False)
    voucher_type_name = serializers.CharField(source='voucher_type', read_only=True)
    voucher_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Voucher
        fields = ['guid', 'voucher_number', 'date', 'voucher_type',
                  'voucher_type_name', 'reference_number', 'reference_date',
                  'narration', 'party_name', 'place_of_supply',
                  'is_invoice', 'is_accounting_voucher', 'is_inventory_voucher',
                  'is_order_voucher', 'financial_year', 'created_by', 'status',
                  'items', 'created_at']
        read_only_fields = ['guid', 'created_by', 'created_at']

    def validate_items(self, items):
        if items:
            dr = sum(i['amount'] for i in items if i.get('is_dr', True))
            cr = sum(i['amount'] for i in items if not i.get('is_dr', True))
            # Only enforce double-entry when both sides are present.
            if dr and cr and abs(dr - cr) > 0.01:
                raise serializers.ValidationError(
                    f'Debit ({dr}) and Credit ({cr}) totals must be equal.')
        return items

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('accounting_entries', [])
        if not validated_data.get('voucher_number'):
            validated_data['voucher_number'] = next_voucher_number(validated_data.get('voucher_type'))
        voucher = Voucher.objects.create(**validated_data)
        for item in items_data:
            AccountingEntry.objects.create(voucher=voucher, **item)
        return voucher

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop('accounting_entries', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items_data is not None:  # replace entries only when sent
            instance.accounting_entries.all().delete()
            for item in items_data:
                AccountingEntry.objects.create(voucher=instance, **item)
        return instance
