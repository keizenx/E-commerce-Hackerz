"""
Tests d'intégration pour les vues de coupons (apply_coupon, remove_coupon, validate_coupon_ajax)
Ces tests vérifient l'intégration entre les vues de coupons, les modèles Coupon et la session.
"""
import json
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from Hackerz_E_commerce.models import Category, Product, Cart, CartItem, Coupon


@pytest.mark.django_db
class TestApplyCouponView:
    """Tests d'intégration pour la vue apply_coupon"""
    
    def test_apply_coupon_valid(self, client):
        """Test que apply_coupon applique un coupon valide"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("100.00"),
            price=Decimal("80.00"),
            stock=10,
            available=True
        )
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        # Créer un coupon valide
        coupon = Coupon.objects.create(
            code="TEST10",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            min_purchase=Decimal("50.00"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
            active=True
        )
        
        response = client.post(reverse('shop:apply_coupon'), {
            'coupon_code': 'TEST10'
        })
        
        assert response.status_code == 302  # Redirection
        assert 'coupon_id' in client.session
        assert client.session['coupon_id'] == coupon.id
    
    def test_apply_coupon_invalid_code(self, client):
        """Test que apply_coupon rejette un code invalide"""
        response = client.post(reverse('shop:apply_coupon'), {
            'coupon_code': 'INVALID'
        })
        
        assert response.status_code == 302  # Redirection avec message d'erreur
    
    def test_apply_coupon_min_purchase_not_met(self, client):
        """Test que apply_coupon rejette si le montant minimum n'est pas atteint"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Cheap Product",
            slug="cheap-product",
            category=category,
            regular_price=Decimal("20.00"),
            price=Decimal("15.00"),
            stock=10,
            available=True
        )
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        # Créer un coupon avec montant minimum élevé
        coupon = Coupon.objects.create(
            code="MIN50",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            min_purchase=Decimal("50.00"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
            active=True
        )
        
        response = client.post(reverse('shop:apply_coupon'), {
            'coupon_code': 'MIN50'
        })
        
        assert response.status_code == 302  # Redirection avec message d'erreur


@pytest.mark.django_db
class TestRemoveCouponView:
    """Tests d'intégration pour la vue remove_coupon"""
    
    def test_remove_coupon(self, client):
        """Test que remove_coupon retire le coupon de la session"""
        coupon = Coupon.objects.create(
            code="TEST10",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            min_purchase=Decimal("50.00"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
            active=True
        )
        
        # Ajouter le coupon à la session
        session = client.session
        session['coupon_id'] = coupon.id
        session['coupon_code'] = coupon.code
        session.save()
        
        response = client.post(reverse('shop:remove_coupon'))
        
        assert response.status_code == 302  # Redirection
        assert 'coupon_id' not in client.session
        assert 'coupon_code' not in client.session


@pytest.mark.django_db
class TestValidateCouponAjaxView:
    """Tests d'intégration pour la vue validate_coupon_ajax"""
    
    def test_validate_coupon_ajax_valid(self, client):
        """Test que validate_coupon_ajax valide un coupon valide"""
        coupon = Coupon.objects.create(
            code="VALID10",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            min_purchase=Decimal("50.00"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
            active=True
        )
        
        response = client.post(
            reverse('shop:validate_coupon'),
            {'coupon_code': 'VALID10'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['message'] == 'Code promo valide'
        assert data['discount_type'] == 'percentage'
        assert float(data['discount_value']) == 10.0
    
    def test_validate_coupon_ajax_invalid(self, client):
        """Test que validate_coupon_ajax rejette un coupon invalide"""
        response = client.post(
            reverse('shop:validate_coupon'),
            {'coupon_code': 'INVALID'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is False
        assert 'invalide' in data['message'].lower()
    
    def test_validate_coupon_ajax_expired(self, client):
        """Test que validate_coupon_ajax rejette un coupon expiré"""
        coupon = Coupon.objects.create(
            code="EXPIRED",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            min_purchase=Decimal("50.00"),
            valid_from=timezone.now() - timedelta(days=30),
            valid_to=timezone.now() - timedelta(days=1),  # Expiré
            active=True
        )
        
        response = client.post(
            reverse('shop:validate_coupon'),
            {'coupon_code': 'EXPIRED'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is False

