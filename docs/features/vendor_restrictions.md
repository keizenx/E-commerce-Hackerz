# Restrictions pour les Vendeurs

**Emplacement:** `/docs/features/vendor_restrictions.md`  
**Description:** Documentation sur les restrictions appliquées aux vendeurs  
**Pourquoi:** Garantir l'intégrité du système et éviter les conflits d'intérêt  
**RELEVANT FILES:** Hackerz_E_commerce/views.py, Hackerz/models.py, tests/unit/test_vendor_own_products.py

---

## Vue d'ensemble

Ce document décrit les restrictions appliquées aux vendeurs sur la plateforme Vectal E-Commerce pour maintenir l'intégrité du système et éviter les conflits d'intérêt.

## Restriction principale: Pas d'auto-achat

### Règle

**Un vendeur ne peut PAS commander ses propres produits.**

Cette règle s'applique à toutes les méthodes d'ajout au panier:
- `add_to_cart` - Ajout standard au panier
- `cart_add` - Ajout via AJAX
- `buy_now` - Achat immédiat

### Justification

1. **Éviter les conflits d'intérêt** - Un vendeur ne devrait pas générer des ventes artificielles
2. **Intégrité des données** - Éviter les manipulations des statistiques de vente
3. **Expérience utilisateur** - Clarifier les rôles (vendeur vs acheteur)

### Implémentation technique

#### Vérification dans les vues

Chaque fonction d'ajout au panier vérifie si:
1. L'utilisateur est connecté
2. L'utilisateur a un profil
3. Le profil a un vendor associé
4. Le vendor du produit correspond au vendor de l'utilisateur

```python
# Exemple de vérification
if product.vendor and hasattr(request.user, 'profile') and hasattr(request.user.profile, 'vendor'):
    if product.vendor == request.user.profile.vendor:
        # Rejeter la requête
        return JsonResponse({
            'success': False,
            'message': "Vous ne pouvez pas commander vos propres produits."
        }, status=403)
```

#### Réponses selon le type de requête

**Requête AJAX:**
- Status code: `403 Forbidden`
- Réponse JSON avec message d'erreur

**Requête standard:**
- Redirection vers la page du produit
- Message flash d'erreur affiché à l'utilisateur

### Messages d'erreur

**Français:**
> "Vous ne pouvez pas commander vos propres produits."

### Test de la fonctionnalité

Des tests unitaires ont été créés dans `tests/unit/test_vendor_own_products.py` pour vérifier:

1. ✅ Un vendor ne peut pas ajouter son propre produit au panier
2. ✅ Un vendor ne peut pas ajouter son propre produit via AJAX
3. ✅ Un vendor PEUT ajouter les produits d'autres vendeurs
4. ✅ Un utilisateur normal PEUT commander les produits d'un vendor
5. ✅ Un vendor ne peut pas utiliser "buy_now" sur son propre produit
6. ✅ Un vendor ne peut pas utiliser "cart_add" sur son propre produit

### Lancer les tests

```bash
# Lancer tous les tests
python manage.py test tests.unit.test_vendor_own_products

# Lancer un test spécifique
python manage.py test tests.unit.test_vendor_own_products.VendorOwnProductsTest.test_vendor_cannot_add_own_product_to_cart
```

## Cas d'usage

### Scénario 1: Vendor tente d'acheter son propre produit

1. **Action:** Le vendor clique sur "Ajouter au panier" sur son propre produit
2. **Résultat:** Redirection vers la page du produit avec message d'erreur
3. **Message:** "Vous ne pouvez pas commander vos propres produits."

### Scénario 2: Vendor achète un produit d'un autre vendor

1. **Action:** Le vendor clique sur "Ajouter au panier" sur le produit d'un autre vendor
2. **Résultat:** Le produit est ajouté au panier normalement
3. **Message:** "Produit ajouté au panier avec succès"

### Scénario 3: Client normal achète un produit d'un vendor

1. **Action:** Un client clique sur "Ajouter au panier" sur un produit
2. **Résultat:** Le produit est ajouté au panier normalement
3. **Message:** "Produit ajouté au panier avec succès"

## Extensions futures possibles

### Idées pour améliorer cette fonctionnalité

1. **Dashboard vendor** - Afficher un avertissement si le vendor consulte ses propres produits
2. **Mode test** - Permettre aux vendors de tester le processus d'achat sans créer de vraies commandes
3. **Statistiques** - Logger les tentatives d'auto-achat pour détecter les comportements suspects
4. **Notifications admin** - Alerter les admins si un vendor tente fréquemment d'acheter ses propres produits

## Notes de développement

### Fichiers modifiés

- `Hackerz_E_commerce/views.py` - Ajout des vérifications dans add_to_cart, cart_add, buy_now
- `tests/unit/test_vendor_own_products.py` - Tests unitaires pour la fonctionnalité

### Points d'attention

- La vérification utilise `hasattr()` pour éviter les erreurs si le profil ou le vendor n'existe pas
- Les produits sans vendor (produits de la plateforme) peuvent être commandés par tout le monde
- Cette restriction ne s'applique QU'aux produits avec un vendor associé

## Support & Questions

Pour toute question sur cette fonctionnalité, consulter:
- Code source: `Hackerz_E_commerce/views.py`
- Tests: `tests/unit/test_vendor_own_products.py`
- Modèles: `Hackerz/models.py` (Vendor, Profile)
