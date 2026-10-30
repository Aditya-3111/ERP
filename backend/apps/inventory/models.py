from django.db import models
import uuid


class UnitOfMeasure(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    formal_name = models.CharField(max_length=100, blank=True)
    is_simple_unit = models.BooleanField(default=True)
    base_units = models.CharField(max_length=100, blank=True)
    additional_units = models.CharField(max_length=100, blank=True)
    conversion = models.DecimalField(max_digits=15, decimal_places=4, default=1)

    class Meta:
        db_table = 'inv_uom'

    def __str__(self):
        return self.name


class StockGroup(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'inv_stock_groups'

    def __str__(self):
        return self.name


class StockCategory(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'inv_stock_categories'

    def __str__(self):
        return self.name


class Godown(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    incharge = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'inv_godowns'

    def __str__(self):
        return self.name


class StockItem(models.Model):
    COSTING_CHOICES = [
        ('FIFO', 'FIFO'),
        ('LIFO', 'LIFO'),
        ('Average', 'Average'),
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, blank=True)
    alias = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    part_number = models.CharField(max_length=100, blank=True)
    uom = models.CharField(max_length=50, blank=True)
    alternate_uom = models.CharField(max_length=50, blank=True)
    conversion = models.DecimalField(max_digits=15, decimal_places=4, default=1)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    opening_rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    opening_value = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    closing_rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    closing_value = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    costing_method = models.CharField(max_length=20, default='FIFO', choices=COSTING_CHOICES)
    gst_type_of_supply = models.CharField(max_length=50, blank=True)
    gst_hsn_code = models.CharField(max_length=20, blank=True)
    gst_hsn_description = models.CharField(max_length=255, blank=True)
    gst_rate = models.DecimalField(max_digits=9, decimal_places=4, default=0)
    gst_taxability = models.CharField(max_length=50, blank=True)
    default_godown = models.CharField(max_length=100, blank=True)
    min_stock = models.DecimalField(max_digits=15, decimal_places=4, default=10)
    max_stock = models.DecimalField(max_digits=15, decimal_places=4, default=1000)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='stock_items/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_stock_items'

    def __str__(self):
        return self.name


class StockJournal(models.Model):
    TYPE_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
        ('TRANSFER', 'Transfer'),
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    godown = models.CharField(max_length=100, blank=True)
    destination_godown = models.CharField(max_length=100, blank=True)
    reference = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inv_stock_journals'
        ordering = ['-date', '-created_at']


class StockBatch(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_no = models.CharField(max_length=100)
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    mfg_date = models.DateField(null=True)
    exp_date = models.DateField(null=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    godown = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'inv_stock_batches'

    def __str__(self):
        return f"{self.batch_no} - {self.item_name}"


class MaterialReceiptNote(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mrn_no = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    supplier_name = models.CharField(max_length=200)
    supplier_invoice = models.CharField(max_length=100, blank=True)
    transporter = models.CharField(max_length=100, blank=True)
    vehicle_no = models.CharField(max_length=20, blank=True)
    godown = models.CharField(max_length=100, blank=True)
    eway_bill = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inv_mrn_entries'

    def __str__(self):
        return self.mrn_no


class MRNItem(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mrn = models.ForeignKey(MaterialReceiptNote, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    hsn = models.CharField(max_length=20, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=9, decimal_places=4, default=0)
    gst_amount = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    class Meta:
        db_table = 'inv_mrn_items'