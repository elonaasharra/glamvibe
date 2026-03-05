from django.db import models
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name or "Category"

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    categories = models.ManyToManyField("Category", related_name="products", blank=True)

    main_image = models.ImageField(upload_to="products/main/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name or "Product"

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} x {self.quantity}"