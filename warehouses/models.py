from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Materials(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductMaterials(models.Model):
    product_id = models.ForeignKey('warehouses.Product', on_delete=models.CASCADE)
    material = models.ForeignKey('warehouses.Materials', on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        unique_together = [('product_id', 'material')]

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than 0")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_id.name


class WareHouses(models.Model):
    material_id = models.ForeignKey('warehouses.Materials', on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.FloatField()

    def save(self, *args, **kwargs):
        if self.remainder <= 0:
            raise ValidationError("Remainder must be greater than 0")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.material_id.name


class Numerator(models.Model):
    warehouse = models.ForeignKey('warehouses.WareHouses', on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return str(self.warehouse)





