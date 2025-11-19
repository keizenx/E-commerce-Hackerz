"""
Tests d'intégration pour la vue add_review
Ces tests vérifient l'intégration entre la vue add_review, les modèles Review et Product.
"""
import json
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from Hackerz_E_commerce.models import Category, Product, Review


@pytest.mark.django_db
class TestAddReviewView:
    """Tests d'intégration pour la vue add_review"""
    
    def test_add_review_requires_login(self, client):
        """Test que add_review exige une authentification"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        
        response = client.post(
            reverse('shop:add_review', args=[product.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 401
    
    def test_add_review_ajax(self, client):
        """Test que add_review ajoute un avis via AJAX"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        client.login(username='testuser', password='testpass')
        
        response = client.post(
            reverse('shop:add_review', args=[product.id]),
            data=json.dumps({
                'rating': 5,
                'title': 'Great product',
                'comment': 'I love it!'
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert Review.objects.filter(product=product, user=user).exists()
    
    def test_add_review_updates_existing(self, client):
        """Test que add_review met à jour un avis existant"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        client.login(username='testuser', password='testpass')
        
        # Créer un avis initial
        review = Review.objects.create(
            product=product,
            user=user,
            rating=3,
            title='Original',
            comment='Original comment',
            active=True
        )
        
        # Mettre à jour l'avis
        response = client.post(
            reverse('shop:add_review', args=[product.id]),
            data=json.dumps({
                'rating': 5,
                'title': 'Updated',
                'comment': 'Updated comment'
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        review.refresh_from_db()
        assert review.rating == 5
        assert review.title == 'Updated'
    
    def test_add_review_invalid_rating(self, client):
        """Test que add_review rejette une note invalide"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        client.login(username='testuser', password='testpass')
        
        response = client.post(
            reverse('shop:add_review', args=[product.id]),
            data=json.dumps({
                'rating': 10,  # Invalide (doit être entre 1 et 5)
                'title': 'Test',
                'comment': 'Test comment'
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
    
    def test_add_review_empty_title(self, client):
        """Test que add_review rejette un titre vide"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        client.login(username='testuser', password='testpass')
        
        response = client.post(
            reverse('shop:add_review', args=[product.id]),
            data=json.dumps({
                'rating': 5,
                'title': '',  # Vide
                'comment': 'Test comment'
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False

