"""
Tests d'intégration pour les vues vendeur (vendor_products, add_product, edit_product, delete_product, vendor_product_detail)
Ces tests vérifient l'intégration entre les vues vendeur, les modèles Product/Vendor et les permissions.
"""
import json
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, Order, OrderItem, Review
from Hackerz.models import Profile, Vendor


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestVendorProductsView:
    """Tests d'intégration pour la vue vendor_products"""
    
    def test_vendor_products_requires_approval(self, client):
        """Test que vendor_products exige un vendeur approuvé"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=False)
        client.login(username='testuser', password='testpass')
        
        url = reverse('shop:vendor_products')
        response = client.get(url)
        
        assert response.status_code == 302  # Redirection
    
    def test_vendor_products_lists_own_products(self, client):
        """Test que vendor_products liste uniquement les produits du vendeur"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=True)
        client.login(username='testuser', password='testpass')
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="My Product",
            slug="my-product",
            category=category,
            vendor=vendor,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        
        url = reverse('shop:vendor_products')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'products' in response.context
        products = list(response.context['products'])
        assert product in products


@pytest.mark.django_db
class TestAddProductView:
    """Tests d'intégration pour la vue add_product"""
    
    def test_add_product_requires_approval(self, client):
        """Test que add_product exige un vendeur approuvé"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=False)
        client.login(username='testuser', password='testpass')
        
        url = reverse('shop:add_product')
        response = client.get(url)
        
        assert response.status_code == 302  # Redirection
    
    def test_add_product_ajax(self, client):
        """Test que add_product crée un produit via AJAX"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=True)
        client.login(username='testuser', password='testpass')
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        
        response = client.post(
            reverse('shop:add_product'),
            {
                'name': 'New Product',
                'category': category.id,
                'price': '99.99',
                'regular_price': '119.99',
                'stock': '10',
                'description': 'Test description',
                'available': 'on',
                'image': image
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert Product.objects.filter(name='New Product', vendor=vendor).exists()
    
    def test_add_product_get_form(self, client):
        """Test que add_product affiche le formulaire en GET"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=True)
        client.login(username='testuser', password='testpass')
        
        url = reverse('shop:add_product')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'categories' in response.context


@pytest.mark.django_db
class TestEditProductView:
    """Tests d'intégration pour la vue edit_product"""
    
    def test_edit_product(self, client):
        """Test que edit_product modifie un produit"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=True)
        client.login(username='testuser', password='testpass')
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Original Product",
            slug="original-product",
            category=category,
            vendor=vendor,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        
        response = client.post(
            reverse('shop:edit_product', args=[product.id]),
            {
                'name': 'Updated Product',
                'category': category.id,
                'price': '89.99',
                'regular_price': '109.99',
                'stock': '15',
                'description': 'Updated description',
                'available': 'on'
            }
        )
        
        assert response.status_code == 302  # Redirection après succès
        product.refresh_from_db()
        assert product.name == 'Updated Product'
        assert product.price == Decimal('89.99')
    
    def test_edit_product_only_own_products(self, client):
        """Test qu'un vendeur ne peut modifier que ses propres produits"""
        user1 = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='testpass')
        profile1 = user1.profile  # Profile créé automatiquement via signal
        profile1.is_vendor = True
        profile1.save()
        vendor1 = Vendor.objects.create(profile=profile1, shop_name="Shop 1", is_approved=True)
        
        user2 = User.objects.create_user(username='vendor2', email='vendor2@example.com', password='testpass')
        profile2 = user2.profile  # Profile créé automatiquement via signal
        profile2.is_vendor = True
        profile2.save()
        vendor2 = Vendor.objects.create(profile=profile2, shop_name="Shop 2", is_approved=True)
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Vendor 1 Product",
            slug="vendor-1-product",
            category=category,
            vendor=vendor1,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        
        # Vendor 2 essaie de modifier le produit de Vendor 1
        client.login(username='vendor2', password='testpass')
        response = client.get(reverse('shop:edit_product', args=[product.id]))
        
        assert response.status_code == 404  # Produit non trouvé car pas le propriétaire


@pytest.mark.django_db
class TestDeleteProductView:
    """Tests d'intégration pour la vue delete_product"""
    
    def test_delete_product(self, client):
        """Test que delete_product supprime un produit"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=True)
        client.login(username='testuser', password='testpass')
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Product to Delete",
            slug="product-to-delete",
            category=category,
            vendor=vendor,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        
        product_id = product.id
        # La fonction a été corrigée pour accepter product_id (comme edit_product)
        response = client.post(reverse('shop:delete_product', args=[product.id]))
        
        assert response.status_code == 302  # Redirection après suppression
        assert not Product.objects.filter(id=product_id).exists()


@pytest.mark.django_db
class TestVendorProductDetailView:
    """Tests d'intégration pour la vue vendor_product_detail"""
    
    def test_vendor_product_detail(self, client):
        """Test que vendor_product_detail affiche les détails d'un produit vendeur"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Test Shop", is_approved=True)
        client.login(username='testuser', password='testpass')
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="My Product",
            slug="my-product",
            category=category,
            vendor=vendor,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        
        # Créer quelques ventes et avis pour les statistiques
        # Il faut créer une vraie commande avec OrderItem
        customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='testpass',
            first_name='Customer',
            last_name='Test'
        )
        order = Order.objects.create(
            user=customer,
            first_name='Customer',
            last_name='Test',
            email='customer@example.com',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            paid=True,
            status='processing'
        )
        OrderItem.objects.create(
            order=order,  # OrderItem nécessite une vraie commande
            product=product,
            quantity=5,
            price=product.price
        )
        Review.objects.create(
            product=product,
            user=user,
            rating=4,
            title="Good",
            comment="Nice product",
            active=True
        )
        
        url = reverse('shop:vendor_product_detail', args=[product.id])
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'product' in response.context
        assert response.context['product'] == product
        assert 'total_sales' in response.context
        assert 'average_rating' in response.context

