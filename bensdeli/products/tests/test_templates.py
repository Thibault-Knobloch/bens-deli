import pytest
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.auth.models import User
from products.models import Product


# def test_add_review_is_available_for_logged_in_users():
    # GIVEN
    # Product.objects.create(name="Test Product", desc="Test Desc", price=2.00, spice_level=Product.Spice.MILD)
    # client.login(username=test_user.username, password=strong_pass)

    #WHEN
    # user goes on the product detail page (in views.py it is the product_view view)
# user = User.objects.create_user(username='testuser', password='testpass')
    # THEN
    # user can see the add review button (so in the html i can find the div with class add_review_div)

@pytest.mark.django_db
def test_add_review_is_available_for_logged_in_users():
    # GIVEN
    Product.objects.create(name="Test Product", desc="Test Desc", price=2.00, spice_level=Product.Spice.MILD, image=create_fake_test_image())
    user = User.objects.create_user(username='testuser', password='testpass')

    # Login the user
    client = Client()
    client.login(username='testuser', password='testpass')

    #WHEN  
    response = client.get('/product/1')

    # THEN
    assert b'<div class="add_review_div centered">' in response.content


@pytest.mark.django_db
def test_add_review_not_available_for_not_logged_in_users():
    # GIVEN
    Product.objects.create(name="Test Product", desc="Test Desc", price=2.00, spice_level=Product.Spice.MILD, image=create_fake_test_image())
    
    #WHEN
    client = Client()
    response = client.get('/product/1')

    # THEN
    assert b'<div class="add_review_div centered">' not in response.content


def create_fake_test_image():
    image_data = (
        b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x00\x00'
        b'\x0e\x00\x2c\x00\x00\x00\x00\x02\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
    )

    with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
        f.write(image_data)
        image = SimpleUploadedFile(f.name, f.read(), content_type='image/gif')
    return image
    