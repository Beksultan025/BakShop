from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image


def validate_image_size(file):
    if file.size > 3 * 1024 * 1024:
        raise ValidationError("Фото должно быть не больше 3 МБ")


class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    brand = models.CharField("Бренд", max_length=100)
    car = models.CharField("Подходит для авто", max_length=200)
    price = models.DecimalField("Цена, сом", max_digits=10, decimal_places=0)
    photo = models.ImageField(
        "Фото",
        upload_to="products/",
        blank=True,
        validators=[validate_image_size],
    )
    badge = models.CharField("Метка (Хит, -15%)", max_length=30, blank=True)
    in_stock = models.BooleanField("В наличии", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            if img.width > 800 or img.height > 800:
                img.thumbnail((800, 800))
                img.save(self.photo.path)