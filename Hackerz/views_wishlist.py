"""
Vues pour la gestion de la wishlist (liste de souhaits)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Wishlist
from Hackerz_E_commerce.models import Product


@login_required
def wishlist_view(request):
    """Affiche la liste de souhaits de l'utilisateur"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    context = {
        'wishlist': wishlist,
        'products': products,
        'count': products.count()
    }
    
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """Ajoute un produit à la liste de souhaits"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Ce produit est déjà dans votre liste de souhaits'
            })
        messages.info(request, 'Ce produit est déjà dans votre liste de souhaits')
    else:
        wishlist.products.add(product)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} a été ajouté à votre liste de souhaits',
                'wishlist_count': wishlist.products.count()
            })
        messages.success(request, f'{product.name} a été ajouté à votre liste de souhaits')
    
    # Rediriger vers la page précédente ou la liste de souhaits
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:view'))


@login_required
def remove_from_wishlist(request, product_id):
    """Retire un produit de la liste de souhaits"""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.products.remove(product)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} a été retiré de votre liste de souhaits',
                'wishlist_count': wishlist.products.count()
            })
        messages.success(request, f'{product.name} a été retiré de votre liste de souhaits')
    except Wishlist.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Erreur lors de la suppression'
            })
        messages.error(request, 'Erreur lors de la suppression')
    
    return redirect('wishlist:view')


@login_required
def clear_wishlist(request):
    """Vide complètement la liste de souhaits"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.products.clear()
        messages.success(request, 'Votre liste de souhaits a été vidée')
    except Wishlist.DoesNotExist:
        pass
    
    return redirect('wishlist:view')


@login_required
def toggle_wishlist(request, product_id):
    """Toggle un produit dans la wishlist (ajoute si absent, retire si présent)"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        action = 'removed'
        message = f'{product.name} a été retiré de votre liste de souhaits'
    else:
        wishlist.products.add(product)
        action = 'added'
        message = f'{product.name} a été ajouté à votre liste de souhaits'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'action': action,
            'message': message,
            'wishlist_count': wishlist.products.count(),
            'in_wishlist': action == 'added'
        })
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:view'))
