from django.db import models
from apps.inventory.models import StockItem, Godown
from apps.core.models import User
import uuid


class POSCounter(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    counter_name = models.CharField(max_length=100)
    counter_code = models.CharField(max_length=20, unique=True)
    branch = models.ForeignKey('core.Branch', on_delete=models.SET_NULL, null=True)
    godown = models.ForeignKey(Godown, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, blank=True)
    printer_name = models.CharField(max_length=100, blank=True)
    receipt_header = models.TextField(blank=True)
    receipt_footer = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'pos_counters'

    def __str__(self):
        return self.counter_name


class POSSession(models.Model):
    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed'), ('reconciled', 'Reconciled')]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    counter = models.ForeignKey(POSCounter, on_delete=models.CASCADE)
    session_date = models.DateField()
    opening_time = models.DateTimeField(null=True)
    closing_time = models.DateTimeField(null=True)
    opening_balance = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    closing_balance = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    expected_cash = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    actual_cash = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    cash_difference = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    total_sales = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    total_returns = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    transaction_count = models.IntegerField(default=0)
    opened_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='opened_sessions')
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='closed_sessions')
    status = models.CharField(max_length=20, default='open', choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pos_sessions'


class PriceList(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price_list_name = models.CharField(max_length=100)
    price_list_code = models.CharField(max_length=50, unique=True)
    is_inclusive_tax = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'pos_price_lists'

    def __str__(self):
        return self.price_list_name


class ItemPrice(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    mrp = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    selling_price = models.DecimalField(max_digits=15, decimal_places=4)
    wholesale_price = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    discount_allowed = models.BooleanField(default=True)
    max_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    class Meta:
        db_table = 'pos_item_prices'
        unique_together = ['item', 'price_list']


class POSCustomer(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    customer_type = models.CharField(max_length=20, default='walkin')
    loyalty_points = models.IntegerField(default=0)
    total_purchases = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    last_purchase_date = models.DateField(null=True)

    class Meta:
        db_table = 'pos_customers'

    def __str__(self):
        return self.customer_name or 'Walk-in Customer'


class POSSale(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'), ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'), ('hold', 'Hold')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    invoice_time = models.TimeField(null=True)
    counter = models.ForeignKey(POSCounter, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(POSSession, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(POSCustomer, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=200, blank=True)
    customer_mobile = models.CharField(max_length=15, blank=True)
    subtotal = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    round_off = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    total_items = models.IntegerField(default=0)
    total_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    payment_method = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length=20, default='paid')
    sales_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='completed', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pos_sales'
        ordering = ['-invoice_date', '-created_at']

    def __str__(self):
        return self.invoice_no


class POSSaleItem(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(POSSale, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(StockItem, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=100, blank=True)
    hsn_code = models.CharField(max_length=20, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    uom = models.CharField(max_length=50, blank=True)
    mrp = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    selling_price = models.DecimalField(max_digits=15, decimal_places=4)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=9, decimal_places=4, default=0)
    cgst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=17, decimal_places=2)
    line_total = models.DecimalField(max_digits=17, decimal_places=2)

    class Meta:
        db_table = 'pos_sale_items'


class PaymentMethod(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    method_name = models.CharField(max_length=100)
    method_code = models.CharField(max_length=50, unique=True)
    method_type = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'), ('card', 'Card'), ('upi', 'UPI'),
        ('wallet', 'Wallet'), ('bank_transfer', 'Bank Transfer')
    ])
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'pos_payment_methods'

    def __str__(self):
        return self.method_name


class POSPayment(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(POSSale, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=17, decimal_places=2)
    reference_number = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, default='completed')

    class Meta:
        db_table = 'pos_payments'