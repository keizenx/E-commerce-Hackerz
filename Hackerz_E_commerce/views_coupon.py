"""
Vues pour la gestion des codes promo et coupons
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from .models import Coupon


def apply_coupon(request):
    """Applique un code promo au panier"""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        
        if not coupon_code:
            messages.error(request, 'Veuillez entrer un code promo')
            return redirect('shop:cart_detail')
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            is_valid, message = coupon.is_valid()
            
            if not is_valid:
                messages.error(request, message)
                return redirect('shop:cart_detail')
            
            # Calculer le total du panier
            from .models import Cart, CartItem
            from .views import _cart_id
            
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, active=True)
                total = sum(item.sub_total() for item in cart_items)
                
                # Vérifier le montant minimum
                if total < coupon.min_purchase:
                    messages.error(request, f'Achat minimum de {coupon.min_purchase}€ requis pour utiliser ce code promo')
                    return redirect('shop:cart_detail')
                
                # Stocker le coupon dans la session
                request.session['coupon_id'] = coupon.id
                request.session['coupon_code'] = coupon.code
                
                # Calculer la réduction
                new_total, discount = coupon.apply_discount(total)
                
                messages.success(request, f'Code promo "{coupon.code}" appliqué! Vous économisez {discount:.2f}€')
                
            except Cart.DoesNotExist:
                messages.error(request, 'Votre panier est vide')
                return redirect('shop:shop')
            
        except Coupon.DoesNotExist:
            messages.error(request, 'Code promo invalide')
    
    return redirect('shop:cart_detail')


def remove_coupon(request):
    """Retire le code promo du panier"""
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    
    messages.success(request, 'Code promo retiré')
    return redirect('shop:cart_detail')


def get_coupon_discount(request):
    """
    Fonction utilitaire pour obtenir la réduction du coupon actuel
    Retourne (coupon, discount_amount) ou (None, 0)
    """
    coupon_id = request.session.get('coupon_id')
    
    if not coupon_id:
        return None, Decimal('0')
    
    try:
        coupon = Coupon.objects.get(id=coupon_id)
        is_valid, _ = coupon.is_valid()
        
        if not is_valid:
            # Supprimer le coupon invalide de la session
            if 'coupon_id' in request.session:
                del request.session['coupon_id']
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
            return None, Decimal('0')
        
        return coupon, Decimal('0')  # Le montant sera calculé dans la vue
        
    except Coupon.DoesNotExist:
        return None, Decimal('0')


def validate_coupon_ajax(request):
    """Valide un code promo via AJAX (sans l'appliquer)"""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        
        if not coupon_code:
            return JsonResponse({
                'success': False,
                'message': 'Veuillez entrer un code promo'
            })
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            is_valid, message = coupon.is_valid()
            
            if not is_valid:
                return JsonResponse({
                    'success': False,
                    'message': message
                })
            
            # Informations sur le coupon
            if coupon.discount_type == 'percentage':
                discount_info = f'{coupon.discount_value}% de réduction'
            else:
                discount_info = f'{coupon.discount_value}€ de réduction'
            
            return JsonResponse({
                'success': True,
                'message': 'Code promo valide',
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value),
                'discount_info': discount_info,
                'min_purchase': float(coupon.min_purchase)
            })
            
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Code promo invalide'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée'
    })
