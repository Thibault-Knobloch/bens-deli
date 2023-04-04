from products.views import calculate_average_rating
from products.models import Review, Product

import pytest

@pytest.mark.django_db
def test_calculate_average_review_rating_works():
    # GIVEN
    product = Product.objects.create(name="Test Product", desc="Test Desc", price=2.00, spice_level=Product.Spice.MILD)
    Review.objects.create(name="Reviewer 1", rating=2, product=product)
    Review.objects.create(name="Reviewer 2", rating=2, product=product)
    Review.objects.create(name="Reviewer 3", rating=3, product=product)
    Review.objects.create(name="Reviewer 4", rating=4, product=product)

    #WHEN
    reviews = product.reviews.all()
    avg = calculate_average_rating(reviews)

    # THEN
    assert avg == 2.75
    

@pytest.mark.django_db
def test_calculate_average_review_handles_no_reviews():
    # GIVEN
    product = Product.objects.create(name="Test Product", desc="Test Desc", price=2.00, spice_level=Product.Spice.MILD)

    #WHEN
    reviews = product.reviews.all()
    avg = calculate_average_rating(reviews)

    # THEN
    assert avg == "no rating"