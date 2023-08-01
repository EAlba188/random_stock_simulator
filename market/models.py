
from django.db import models


class StockModel(models.Model):
    name = models.CharField(max_length=50)
    last_price = models.FloatField(default=100)

    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was modified",
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "stock"

    def __str__(self):
        return self.name


class PriceModel(models.Model):
    price = models.FloatField()
    stock_related = models.ForeignKey(StockModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was modified",
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(blank=True, null=True)


class UserModel(models.Model):
    name = models.CharField(max_length=50)
    money = models.FloatField()

    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was modified",
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name