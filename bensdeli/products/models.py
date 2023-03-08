from django.db import models


# Create your models here.
class Product(models.Model):
    class Spice(models.IntegerChoices):
        NO_SPICE = 1
        MILD = 2
        SPICY = 3
        EXTRA_SPICY = 4
        FIRE_SPICE = 5

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    desc = models.TextField()
    image = models.ImageField(upload_to="product_images/")
    price = models.FloatField()

    spice_level = models.IntegerField(choices=Spice.choices)
