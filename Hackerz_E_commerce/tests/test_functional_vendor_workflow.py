"""
Tests fonctionnels pour le workflow complet vendeur
Ces tests vérifient des scénarios complets : création de compte vendeur, approbation, ajout de produits, gestion des ventes.
"""
import json
import pytest
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, Order, OrderItem
from Hackerz.models import Profile, Vendor


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestVendorWorkflow:
    """Tests fonctionnels pour le workflow complet vendeur"""
    
    def test_complete_vendor_workflow(self, client):
        """Test du workflow complet : inscription -> demande vendeur -> approbation -> ajout produit -> vente"""
        # 1. Créer un utilisateur
        user = User.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='testpass',
            first_name='Vendor',
            last_name='Test'
        )
        profile = user.profile  # Profile créé automatiquement via signal
        client.login(username='vendor', password='testpass')
        
        # 2. Créer une demande de vendeur
        vendor = Vendor.objects.create(
            profile=profile,
            shop_name="Test Shop",
            description="Test shop description",
            is_approved=False
        )
        
        # 3. Approuver le vendeur (simulation admin)
        vendor.is_approved = True
        vendor.save()
        profile.is_vendor = True
        profile.save()
        
        # 4. Créer une catégorie
        category = Category.objects.create(name="Electronics", slug="electronics")
        
        # 5. Le vendeur ajoute un produit
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
        product = Product.objects.get(name='New Product', vendor=vendor)
        assert product is not None
        
        # 6. Le vendeur consulte ses produits
        response = client.get(reverse('shop:vendor_products'))
        assert response.status_code == 200
        assert product in response.context['products']
        
        # 7. Simuler une vente (création d'une commande)
        customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='testpass'
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
            order=order,
            product=product,
            quantity=2,
            price=product.price
        )
        
        # 8. Le vendeur consulte les détails de son produit avec statistiques
        response = client.get(reverse('shop:vendor_product_detail', args=[product.id]))
        assert response.status_code == 200
        assert response.context['total_sales'] == 2
        
        # 9. Le vendeur modifie son produit
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
        assert response.status_code == 302
        product.refresh_from_db()
        assert product.name == 'Updated Product'
        assert product.price == Decimal('89.99')
    
    def test_vendor_cannot_access_without_approval(self, client):
        """Test qu'un vendeur non approuvé ne peut pas accéder aux fonctionnalités vendeur"""
        user = User.objects.create_user(username='vendor', email='vendor@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        Vendor.objects.create(
            profile=profile,
            shop_name="Test Shop",
            is_approved=False  # Non approuvé
        )
        client.login(username='vendor', password='testpass')
        
        # Essayer d'accéder à la liste des produits
        response = client.get(reverse('shop:vendor_products'))
        assert response.status_code == 302  # Redirection
        
        # Essayer d'ajouter un produit
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
        # Devrait échouer ou rediriger
        assert response.status_code in [302, 400]

