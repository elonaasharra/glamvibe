from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    categories = models.ManyToManyField("Category", related_name="products")

    main_image = models.ImageField(upload_to="products/main/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class ProductImage(models.Model):
        product = models.ForeignKey(
            "Product",
            on_delete=models.CASCADE,
            related_name="gallery_images"
        )
        image = models.ImageField(upload_to="products/gallery/")

        def __str__(self):
            return f"Image for {self.product.name}"