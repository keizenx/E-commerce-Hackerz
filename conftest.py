"""
Configuration globale pour pytest
"""
import os
import django

# Configuration de Django avant tout import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hackerz.settings')
django.setup()

import pytest
from django.contrib.auth.models import User
from django.test import Client
from decimal import Decimal

from Hackerz_E_commerce.models import (
    Category, Product, Cart, CartItem, Order, OrderItem, Review
)
from Hackerz.models import Profile, Vendor, Wishlist


@pytest.fixture
def client():
    """Client Django pour les tests."""
    return Client()


@pytest.fixture
def api_client():
    """Client API REST pour les tests."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    """Utilisateur de test standard."""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    return user


@pytest.fixture
def admin_user(db):
    """Utilisateur administrateur pour les tests."""
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    return user


@pytest.fixture
def vendor_user(db):
    """Utilisateur vendeur pour les tests."""
    user = User.objects.create_user(
        username='vendor',
        email='vendor@example.com',
        password='vendorpass123'
    )
    profile = user.profile
    profile.is_vendor = True
    profile.save()
    
    vendor = Vendor.objects.create(
        profile=profile,
        shop_name='Test Shop',
        description='Test shop description',
        is_approved=True
    )
    return user


@pytest.fixture
def category(db):
    """Catégorie de produits pour les tests."""
    return Category.objects.create(
        name='Electronics',
        slug='electronics',
        description='Electronic products'
    )


@pytest.fixture
def product(db, category, vendor_user):
    """Produit pour les tests."""
    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image
    import io
    
    vendor = vendor_user.profile.vendor
    
    # Create a test image
    image = Image.new('RGB', (100, 100), color='red')
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    test_image = SimpleUploadedFile("test_product.jpg", image_io.read(), content_type="image/jpeg")
    
    return Product.objects.create(
        vendor=vendor,
        category=category,
        name='Test Product',
        slug='test-product',
        description='Test product description',
        regular_price=Decimal('100.00'),
        price=Decimal('89.99'),
        stock=50,
        available=True,
        featured=False,
        image=test_image
    )


@pytest.fixture
def products(db, category, vendor_user):
    """Multiple produits pour les tests."""
    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image
    import io
    
    vendor = vendor_user.profile.vendor
    products_list = []
    for i in range(5):
        # Create a test image for each product
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        test_image = SimpleUploadedFile(f"test_product_{i}.jpg", image_io.read(), content_type="image/jpeg")
        
        product = Product.objects.create(
            vendor=vendor,
            category=category,
            name=f'Product {i+1}',
            slug=f'product-{i+1}',
            description=f'Description for product {i+1}',
            regular_price=Decimal(f'{100 + i*10}.00'),
            price=Decimal(f'{90 + i*10}.00'),
            stock=50 - i*5,
            available=True,
            featured=i % 2 == 0,
            image=test_image
        )
        products_list.append(product)
    return products_list


@pytest.fixture
def cart(db):
    """Panier pour les tests."""
    return Cart.objects.create(
        cart_id='test-cart-123'
    )


@pytest.fixture
def cart_with_items(db, cart, product):
    """Panier avec des items pour les tests."""
    CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2,
        active=True
    )
    return cart


@pytest.fixture
def order(db, user):
    """Commande pour les tests."""
    return Order.objects.create(
        user=user,
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        address='123 Test Street',
        postal_code='75001',
        city='Paris',
        paid=False,
        status='pending'
    )


@pytest.fixture
def order_with_items(db, order, product):
    """Commande avec des items pour les tests."""
    OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        quantity=2
    )
    return order


@pytest.fixture
def review(db, product, user):
    """Avis produit pour les tests."""
    return Review.objects.create(
        product=product,
        user=user,
        rating=5,
        title='Great product!',
        comment='This is an excellent product.',
        active=True
    )


@pytest.fixture
def authenticated_client(client, user):
    """Client Django authentifié."""
    client.force_login(user)
    return client


@pytest.fixture
def authenticated_api_client(api_client, user):
    """Client API authentifié."""
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_api_client(api_client, admin_user):
    """Client API avec droits admin."""
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def wishlist(db, user):
    """Wishlist pour les tests."""
    return Wishlist.objects.create(user=user)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Permet l'accès à la DB pour tous les tests."""
    pass


@pytest.fixture
def mock_session(client):
    """Session Django mockée."""
    session = client.session
    session['cart_id'] = 'test-cart-123'
    session.save()
    return session


# Helpers pour les tests

@pytest.fixture
def create_user():
    """Factory pour créer des utilisateurs."""
    def _create_user(username=None, email=None, password='testpass123', **kwargs):
        if username is None:
            import uuid
            username = f'user_{uuid.uuid4().hex[:8]}'
        if email is None:
            email = f'{username}@example.com'
        
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
    return _create_user


@pytest.fixture
def create_product():
    """Factory pour créer des produits."""
    def _create_product(category, vendor=None, **kwargs):
        defaults = {
            'name': 'Test Product',
            'slug': 'test-product',
            'description': 'Test description',
            'regular_price': Decimal('100.00'),
            'price': Decimal('89.99'),
            'stock': 50,
            'available': True
        }
        defaults.update(kwargs)
        
        if vendor is None and 'vendor' not in kwargs:
            defaults.pop('vendor', None)
        
        return Product.objects.create(
            category=category,
            vendor=vendor,
            **defaults
        )
    return _create_product


@pytest.fixture
def create_category():
    """Factory pour créer des catégories."""
    def _create_category(**kwargs):
        defaults = {
            'name': 'Test Category',
            'slug': 'test-category',
            'description': 'Test category description'
        }
        defaults.update(kwargs)
        return Category.objects.create(**defaults)
    return _create_category
