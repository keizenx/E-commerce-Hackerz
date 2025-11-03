// =============================================================================
// Django Hackerz E-Commerce - JavaScript Principal
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Hackerz E-Commerce - JS chargé');
    
    // CSRF Token pour les requêtes AJAX
    const csrftoken = getCookie('csrftoken');
    
    // Initialiser les fonctionnalités
    initWishlist();
    initCart();
    initCoupon();
});

// =============================================================================
// UTILITAIRES
// =============================================================================

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type = 'info') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// =============================================================================
// WISHLIST
// =============================================================================

function initWishlist() {
    // Toggle wishlist buttons
    document.querySelectorAll('[data-wishlist-toggle]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            toggleWishlist(productId, this);
        });
    });
}

function toggleWishlist(productId, button) {
    fetch(`/wishlist/toggle/${productId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update button appearance
            const icon = button.querySelector('i');
            if (data.in_wishlist) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
                button.classList.add('text-danger');
            } else {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
                button.classList.remove('text-danger');
            }
            
            // Update wishlist count
            updateWishlistCount(data.wishlist_count);
            showToast(data.message, 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Erreur lors de la mise à jour de la wishlist', 'danger');
    });
}

function updateWishlistCount(count) {
    const badge = document.querySelector('.wishlist-count');
    if (badge) {
        badge.textContent = count;
        if (count > 0) {
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    }
}

// =============================================================================
// CART
// =============================================================================

function initCart() {
    // Add to cart buttons
    document.querySelectorAll('[data-cart-add]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;
            addToCart(productId, quantity);
        });
    });
}

function addToCart(productId, quantity = 1) {
    fetch(`/shop/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCount(data.cart_count);
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'warning');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Erreur lors de l\'ajout au panier', 'danger');
    });
}

function updateCartCount(count) {
    const badge = document.querySelector('.cart-count');
    if (badge) {
        badge.textContent = count;
        if (count > 0) {
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    }
}

// =============================================================================
// COUPONS
// =============================================================================

function initCoupon() {
    const couponForm = document.getElementById('coupon-form');
    if (couponForm) {
        couponForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const code = this.querySelector('[name="coupon_code"]').value;
            validateCoupon(code);
        });
    }
}

function validateCoupon(code) {
    fetch('/shop/coupon/validate/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `coupon_code=${encodeURIComponent(code)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(`Code promo valide: ${data.discount_info}`, 'success');
            // Apply the coupon
            document.getElementById('coupon-form').submit();
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Erreur lors de la validation du code promo', 'danger');
    });
}

// =============================================================================
// PRODUCT RATING
// =============================================================================

function initRating() {
    document.querySelectorAll('.star-rating').forEach(container => {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[name="rating"]');
        
        stars.forEach(star => {
            star.addEventListener('click', function() {
                const rating = this.dataset.rating;
                input.value = rating;
                updateStars(stars, rating);
            });
        });
    });
}

function updateStars(stars, rating) {
    stars.forEach(star => {
        if (star.dataset.rating <= rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}
