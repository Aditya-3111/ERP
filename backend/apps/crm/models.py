from django.db import models
import uuid


class Customer(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    customer_type = models.CharField(max_length=20, default='customer', choices=[
        ('customer', 'Customer'), ('supplier', 'Supplier'), ('both', 'Both')
    ])
    contact_person = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    alt_mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    source = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    address_billing = models.TextField(blank=True)
    address_shipping = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default='India')
    gstin = models.CharField(max_length=15, blank=True)
    pan = models.CharField(max_length=10, blank=True)
    msme_no = models.CharField(max_length=50, blank=True)
    credit_limit = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    credit_period = models.IntegerField(default=30)
    payment_terms = models.CharField(max_length=100, blank=True)
    price_category = models.CharField(max_length=50, blank=True)
    tax_registration_type = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=50, blank=True)
    bank_ifsc = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='active', choices=[
        ('active', 'Active'), ('inactive', 'Inactive'), ('blocked', 'Blocked')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_customers'

    def __str__(self):
        return self.name


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'), ('contacted', 'Contacted'), ('qualified', 'Qualified'),
        ('converted', 'Converted'), ('lost', 'Lost')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    source = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='new', choices=STATUS_CHOICES)
    priority = models.CharField(max_length=10, default='medium', choices=[
        ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')
    ])
    assigned_to = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_leads'

    def __str__(self):
        return self.company


class Activity(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=200, blank=True)
    activity_type = models.CharField(max_length=20, default='Call', choices=[
        ('Call', 'Call'), ('Email', 'Email'), ('Meeting', 'Meeting'),
        ('Visit', 'Visit'), ('Other', 'Other')
    ])
    subject = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_activities'


class Quotation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('approved', 'Approved'),
        ('rejected', 'Rejected'), ('converted', 'Converted')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote_no = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    valid_upto = models.DateField(null=True)
    customer_name = models.CharField(max_length=200)
    customer_contact = models.CharField(max_length=100, blank=True)
    customer_mobile = models.CharField(max_length=15, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_gstin = models.CharField(max_length=15, blank=True)
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)
    reference = models.CharField(max_length=200, blank=True)
    payment_terms = models.CharField(max_length=200, blank=True)
    delivery_terms = models.CharField(max_length=200, blank=True)
    delivery_time = models.CharField(max_length=100, blank=True)
    freight = models.CharField(max_length=100, blank=True)
    warranty = models.CharField(max_length=100, blank=True)
    subtotal = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    prepared_by = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_quotations'

    def __str__(self):
        return self.quote_no


class QuotationItem(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    hsn = models.CharField(max_length=20, blank=True)
    qty = models.DecimalField(max_digits=15, decimal_places=4, default=1)
    uom = models.CharField(max_length=50, blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=9, decimal_places=4, default=0)
    gst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    class Meta:
        db_table = 'crm_quotation_items'


class PurchaseInquiry(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'), ('approved', 'Approved'), ('rejected', 'Rejected'),
        ('closed', 'Closed'), ('converted', 'Converted')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inquiry_no = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    supplier_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    gstin = models.CharField(max_length=15, blank=True)
    item_required = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    expected_rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    expected_date = models.DateField(null=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='open', choices=STATUS_CHOICES)
    priority = models.CharField(max_length=10, default='medium')
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'crm_purchase_inquiries'

    def __str__(self):
        return self.inquiry_no


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'), ('received', 'Received'), ('cancelled', 'Cancelled')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_no = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    delivery_date = models.DateField(null=True)
    reference = models.CharField(max_length=200, blank=True)
    supplier_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    gstin = models.CharField(max_length=15, blank=True)
    supplier_address = models.TextField(blank=True)
    payment_terms = models.CharField(max_length=200, blank=True)
    delivery_terms = models.CharField(max_length=200, blank=True)
    freight = models.CharField(max_length=100, blank=True)
    subtotal = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='open', choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_purchase_orders'

    def __str__(self):
        return self.po_no


class PurchaseOrderItem(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    hsn = models.CharField(max_length=20, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=9, decimal_places=4, default=0)
    gst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    class Meta:
        db_table = 'crm_po_items'