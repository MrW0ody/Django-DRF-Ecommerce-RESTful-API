from django.db import models
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from product.fields import OrderField


class IsActiveQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=235, unique=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    objects = IsActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=235)
    slug = models.SlugField(max_length=255)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(
        "Category", on_delete=models.PROTECT, null=True, blank=True
    )
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='product_type')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    attribute_value = models.ManyToManyField('AttributeValue', through='ProductAttributeValue',
                                             related_name='product_attr_value', blank=True)
    objects = IsActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=10)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)
    weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='product_line_type')
    attribute_value = models.ManyToManyField('AttributeValue', through='ProductLineAttributeValue',
                                             related_name='product_line_attribute_value', blank=True)
    objects = IsActiveQueryset.as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    attribute = models.ManyToManyField('Attribute', through='ProductTypeAttribute',
                                       related_name='product_type_attribute',
                                       blank=True)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default='test.jpg')
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_for_field='product_line', blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.product_line.sku}_img'


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='attribute_value')

    def __str__(self) -> str:
        return f'{self.attribute}-{self.attribute_value}'


class ProductAttributeValue(models.Model):
    attribute_value = models.ForeignKey('AttributeValue', on_delete=models.CASCADE,
                                        related_name='product_value_av')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_value_pl')

    class Meta:
        unique_together = ('attribute_value', 'product')


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey('AttributeValue', on_delete=models.CASCADE,
                                        related_name='product_attribute_value_av')
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE, related_name='product_attribute_value_pl')

    class Meta:
        unique_together = ('attribute_value', 'product_line')

    def clean(self):
        qs = ProductLineAttributeValue.objects.filter(attribute_value=self.attribute_value).filter(
            product_line=self.product_line).exists()
        if not qs:
            iqs = Attribute.objects.filter(attribute_value__product_line_attribute_value=self.product_line).values_list(
                'pk', flat=True)
            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError('Duplicate attribute exists')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, related_name='product_type_attribute_pt')
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='product_type_attribute_a')

    class Meta:
        unique_together = ('product_type', 'attribute')
