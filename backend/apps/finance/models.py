from django.db import models
from apps.core.models import User, FinancialYear
import uuid


class AccountGroup(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    parent = models.CharField(max_length=200, blank=True)
    primary_group = models.CharField(max_length=200, blank=True)
    is_revenue = models.BooleanField(default=False)
    is_deemed_positive = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    affects_gross_profit = models.BooleanField(default=False)
    sort_position = models.IntegerField(default=0)

    class Meta:
        db_table = 'fin_groups'

    def __str__(self):
        return self.name


class Ledger(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    parent = models.CharField(max_length=200, blank=True)
    alias = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_revenue = models.BooleanField(default=False)
    is_deemed_positive = models.BooleanField(default=False)

    # Opening Balance
    opening_balance = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    opening_balance_type = models.CharField(max_length=2, default='dr', choices=[('dr', 'Dr'), ('cr', 'Cr')])
    closing_balance = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    # Contact
    mailing_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)

    # Tax
    pan = models.CharField(max_length=10, blank=True)
    gstin = models.CharField(max_length=15, blank=True)
    gst_registration_type = models.CharField(max_length=50, blank=True)
    gst_supply_type = models.CharField(max_length=50, blank=True)
    gst_duty_head = models.CharField(max_length=20, blank=True)
    msme_no = models.CharField(max_length=50, blank=True)

    # Bank
    bank_account_holder = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_ifsc = models.CharField(max_length=20, blank=True)
    bank_swift = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_branch = models.CharField(max_length=200, blank=True)

    # Credit
    bill_credit_period = models.IntegerField(default=0)
    credit_limit = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    # Documents
    gst_certificate = models.FileField(upload_to='documents/gst/', blank=True)
    business_card = models.ImageField(upload_to='documents/cards/', blank=True)
    pan_card = models.FileField(upload_to='documents/pan/', blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fin_ledgers'

    def __str__(self):
        return self.name


class VoucherType(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    parent = models.CharField(max_length=100, blank=True)
    numbering_method = models.CharField(max_length=50, blank=True)
    is_deemed_positive = models.BooleanField(default=False)
    affects_stock = models.BooleanField(default=False)

    class Meta:
        db_table = 'fin_voucher_types'

    def __str__(self):
        return self.name


class Voucher(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    voucher_type = models.CharField(max_length=100)
    voucher_number = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100, blank=True)
    reference_date = models.DateField(null=True, blank=True)
    narration = models.TextField(blank=True)
    party_name = models.CharField(max_length=200, blank=True)
    place_of_supply = models.CharField(max_length=100, blank=True)
    is_invoice = models.BooleanField(default=False)
    is_accounting_voucher = models.BooleanField(default=True)
    is_inventory_voucher = models.BooleanField(default=False)
    is_order_voucher = models.BooleanField(default=False)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='active', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fin_vouchers'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.voucher_number} - {self.voucher_type}"


class AccountingEntry(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='accounting_entries')
    ledger = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=17, decimal_places=2)
    amount_forex = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    currency = models.CharField(max_length=10, default='INR')
    is_dr = models.BooleanField(default=True)
    narration = models.TextField(blank=True)

    class Meta:
        db_table = 'fin_accounting_entries'

    def __str__(self):
        return f"{self.ledger} - {'Dr' if self.is_dr else 'Cr'} {self.amount}"


class InventoryEntry(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='inventory_entries')
    item = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    additional_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    godown = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    order_number = models.CharField(max_length=100, blank=True)
    order_duedate = models.DateField(null=True, blank=True)
    hsn_code = models.CharField(max_length=20, blank=True)
    gst_rate = models.DecimalField(max_digits=9, decimal_places=4, default=0)
    gst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    class Meta:
        db_table = 'fin_inventory_entries'