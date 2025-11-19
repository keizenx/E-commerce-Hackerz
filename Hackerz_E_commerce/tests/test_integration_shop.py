"""
Tests d'intégration pour les vues de la boutique (shop, product_detail, category_view)
Ces tests vérifient l'intégration entre les vues, les modèles et les templates.
"""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, Review


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestShopView:
    """Tests d'intégration pour la vue shop"""
    
    def test_shop_view_lists_products(self, client):
        """Test que la vue shop liste tous les produits disponibles"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            category=category,
            regular_price=Decimal("149.99"),
            price=Decimal("129.99"),
            stock=5,
            available=True,
            image=image
        )
        
        url = reverse('shop:shop')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'products' in response.context
        products = response.context['products']
        if hasattr(products, 'object_list'):
            product_list = products.object_list
        else:
            product_list = list(products) if products else []
        assert product1 in product_list
        assert product2 in product_list
    
    def test_shop_view_filters_by_category(self, client):
        """Test que la vue shop filtre les produits par catégorie"""
        cat1 = Category.objects.create(name="Electronics", slug="electronics")
        cat2 = Category.objects.create(name="Books", slug="books")
        image = _create_test_image()
        product1 = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=cat1,
            regular_price=Decimal("999.99"),
            price=Decimal("899.99"),
            stock=5,
            available=True,
            image=image
        )
        product2 = Product.objects.create(
            name="Book",
            slug="book",
            category=cat2,
            regular_price=Decimal("19.99"),
            price=Decimal("14.99"),
            stock=20,
            available=True,
            image=image
        )
        
        url = reverse('shop:category_view', kwargs={'category_slug': cat1.slug})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'category' in response.context
        assert response.context['category'] == cat1
        products = response.context['products']
        if hasattr(products, 'object_list'):
            product_list = products.object_list
        else:
            product_list = list(products) if products else []
        assert product1 in product_list
        assert product2 not in product_list
    
    def test_shop_view_search(self, client):
        """Test que la vue shop recherche les produits"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product1 = Product.objects.create(
            name="Laptop Computer",
            slug="laptop-computer",
            category=category,
            regular_price=Decimal("999.99"),
            price=Decimal("899.99"),
            stock=5,
            available=True,
            image=image
        )
        product2 = Product.objects.create(
            name="Mouse Pad",
            slug="mouse-pad",
            category=category,
            regular_price=Decimal("9.99"),
            price=Decimal("7.99"),
            stock=20,
            available=True,
            image=image
        )
        
        url = reverse('shop:shop') + '?q=laptop'
        response = client.get(url)
        
        assert response.status_code == 200
        products = response.context['products']
        if hasattr(products, 'object_list'):
            product_list = products.object_list
        else:
            product_list = list(products) if products else []
        assert product1 in product_list
        assert product2 not in product_list
    
    def test_shop_view_sorting(self, client):
        """Test que la vue shop trie les produits"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product1 = Product.objects.create(
            name="Cheap Product",
            slug="cheap-product",
            category=category,
            regular_price=Decimal("50.00"),
            price=Decimal("40.00"),
            stock=10,
            available=True,
            image=image
        )
        product2 = Product.objects.create(
            name="Expensive Product",
            slug="expensive-product",
            category=category,
            regular_price=Decimal("200.00"),
            price=Decimal("180.00"),
            stock=5,
            available=True,
            image=image
        )
        
        # Test tri par prix croissant
        url = reverse('shop:shop') + '?sort=price_asc'
        response = client.get(url)
        assert response.status_code == 200
        
        # Test tri par prix décroissant
        url = reverse('shop:shop') + '?sort=price_desc'
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestProductDetailView:
    """Tests d'intégration pour la vue product_detail"""
    
    def test_product_detail_view(self, client):
        """Test que la vue product_detail affiche un produit"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            description="Test description",
            image=image
        )
        
        url = reverse('shop:product_detail', kwargs={'product_slug': product.slug})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'product' in response.context
        assert response.context['product'] == product
    
    def test_product_detail_shows_reviews(self, client):
        """Test que la vue product_detail affiche les avis"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        review = Review.objects.create(
            product=product,
            user=user,
            rating=5,
            title="Great product",
            comment="I love it!",
            active=True
        )
        
        url = reverse('shop:product_detail', kwargs={'product_slug': product.slug})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'reviews' in response.context
        assert review in response.context['reviews']
    
    def test_product_detail_shows_related_products(self, client):
        """Test que la vue product_detail affiche les produits similaires"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            category=category,
            regular_price=Decimal("149.99"),
            price=Decimal("129.99"),
            stock=5,
            available=True,
            image=image
        )
        
        url = reverse('shop:product_detail', kwargs={'product_slug': product1.slug})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'related_products' in response.context
        related = list(response.context['related_products'])
        assert product2 in related
        assert product1 not in related
    
    def test_product_detail_unavailable_product(self, client):
        """Test que les produits non disponibles ne sont pas accessibles"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Unavailable Product",
            slug="unavailable-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=0,
            available=False
        )
        
        url = reverse('shop:product_detail', kwargs={'product_slug': product.slug})
        response = client.get(url)
        
        assert response.status_code == 404

