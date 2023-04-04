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


class Review(models.Model):
    RATINGS_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=140)
    rating = models.PositiveSmallIntegerField(choices=RATINGS_CHOICES)
    content = models.TextField(max_length=500)

    def __str__(self):
        str_rating = str(self.rating)
        return self.name + " rating: " + str_rating