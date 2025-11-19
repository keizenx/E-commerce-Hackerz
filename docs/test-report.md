# Rapport de tests – Hackerz E-commerce

## 1. Plan de test
- **Objectif** : Valider les fonctionnalités essentielles d'un site e-commerce multirôle (visiteur, client, vendeur, administrateur).
- **Périmètre** : catalogue produits, panier/checkout, coupons modèles, facturation PDF, rôles utilisateurs et notifications vendeurs/admin.
- **Outils** : `pytest`, `pytest-django`, backend email mémoire (`locmem`), mocks `xhtml2pdf`, fixtures `conftest.py`.
- **Commande** : `python -m pytest Hackerz_E_commerce/tests/ -v --cov=Hackerz_E_commerce --cov-report=term-missing`
- **Critères de succès** :
  - Aucun échec sur le tunnel d'achat complet.
  - Règles métier (stock, coupons, factures) respectées.
  - Scénarios vendeurs/admin contrôlés par tests.

## 2. Matrice de risque / priorisation

| ID | Fonctionnalité / scénario testé | Probabilité | Impact | Priorité |
|----|---------------------------------|-------------|--------|----------|
| TC-001 | Génération automatique du slug catégorie | Moyenne | Moyen | Moyenne |
| TC-002 | Description produit rendue en HTML enrichi (Markdown) | Moyenne | Moyen | Moyenne |
| TC-003 | Sous-total panier par ligne exact | Moyenne | Élevé | Haute |
| TC-004 | Représentation textuelle d'un avis produit | Faible | Mineur | Basse |
| TC-005 | Règles de validité coupon (période, limites, calcul) | Élevée | Élevé | Très haute |
| TC-006 | Calcul du coût d'un item de commande | Élevée | Critique | Très haute |
| TC-007 | Total commande = somme des items | Élevée | Critique | Très haute |
| TC-008 | Réponse HTTP de génération facture PDF | Moyenne | Élevé | Haute |
| TC-009 | Sauvegarde disque de la facture PDF | Moyenne | Élevé | Haute |
| TC-010 | Ajout panier (client authentifié) via AJAX retourne le panier mis à jour | Élevée | Élevé | Très haute |
| TC-011 | Retrait panier décrémente la quantité | Moyenne | Moyen | Moyenne |
| TC-012 | Checkout affiche le récapitulatif (total, compteur, lignes) | Moyenne | Élevé | Haute |
| TC-013 | Parcours commande complet (du panier au paiement) | Élevée | Critique | Très haute |
| TC-014 | Ajout panier exige une authentification préalable | Élevée | Élevé | Très haute |
| TC-015 | Produit indisponible bloqué à l'ajout panier | Élevée | Élevé | Très haute |
| TC-016 | Quantité demandée > stock refusée | Élevée | Élevé | Très haute |
| TC-017 | Visiteur redirigé vers login avant le checkout | Élevée | Critique | Très haute |
| TC-018 | Vue shop liste tous les produits disponibles | Élevée | Élevé | Très haute |
| TC-019 | Vue shop filtre les produits par catégorie | Moyenne | Élevé | Haute |
| TC-020 | Vue shop recherche des produits par nom | Moyenne | Élevé | Haute |
| TC-021 | Vue shop trie les produits (prix, nom, date) | Moyenne | Moyen | Moyenne |
| TC-022 | Vue product_detail affiche les détails d'un produit | Élevée | Élevé | Très haute |
| TC-023 | Vue product_detail affiche les avis du produit | Moyenne | Moyen | Moyenne |
| TC-024 | Vue product_detail affiche les produits similaires | Faible | Mineur | Basse |
| TC-025 | Vue product_detail gère les produits indisponibles | Moyenne | Moyen | Moyenne |
| TC-026 | Vue cart_detail affiche un panier vide | Moyenne | Moyen | Moyenne |
| TC-027 | Vue cart_detail affiche un panier avec articles | Élevée | Élevé | Très haute |
| TC-028 | Vue cart_count retourne 0 pour panier vide | Moyenne | Moyen | Moyenne |
| TC-029 | Vue cart_count retourne le nombre d'articles | Élevée | Élevé | Très haute |
| TC-030 | Vue cart_update augmente la quantité d'un article | Élevée | Élevé | Très haute |
| TC-031 | Vue cart_update refuse quantité > stock | Élevée | Élevé | Très haute |
| TC-032 | Vue delete_from_cart supprime un article | Élevée | Élevé | Très haute |
| TC-033 | Vue checkout exige une authentification | Élevée | Critique | Très haute |
| TC-034 | Vue checkout affiche le récapitulatif avec articles | Élevée | Critique | Très haute |
| TC-035 | Vue checkout gère un panier vide | Moyenne | Élevé | Haute |
| TC-036 | Vue process_payment crée une commande | Élevée | Critique | Très haute |
| TC-037 | Vue process_payment met à jour le stock | Élevée | Critique | Très haute |
| TC-038 | Vue payment_success affiche succès avec commande | Élevée | Élevé | Très haute |
| TC-039 | Vue payment_success gère l'absence de commande | Moyenne | Moyen | Moyenne |
| TC-040 | Vue apply_coupon applique un coupon valide | Élevée | Élevé | Très haute |
| TC-041 | Vue apply_coupon refuse un coupon invalide | Élevée | Élevé | Très haute |
| TC-042 | Vue apply_coupon refuse montant minimum non atteint | Élevée | Élevé | Très haute |
| TC-043 | Vue remove_coupon supprime le coupon appliqué | Moyenne | Élevé | Haute |
| TC-044 | Vue validate_coupon_ajax valide un coupon valide | Moyenne | Élevé | Haute |
| TC-045 | Vue validate_coupon_ajax refuse un coupon invalide | Moyenne | Élevé | Haute |
| TC-046 | Vue validate_coupon_ajax refuse un coupon expiré | Moyenne | Élevé | Haute |
| TC-047 | Vue add_review exige une authentification | Élevée | Élevé | Très haute |
| TC-048 | Vue add_review ajoute un avis via AJAX | Élevée | Élevé | Très haute |
| TC-049 | Vue add_review met à jour un avis existant | Moyenne | Moyen | Moyenne |
| TC-050 | Vue add_review refuse une note invalide | Élevée | Élevé | Très haute |
| TC-051 | Vue add_review refuse un titre vide | Moyenne | Moyen | Moyenne |
| TC-052 | Vue buy_now exige une authentification | Élevée | Critique | Très haute |
| TC-053 | Vue buy_now crée un panier et redirige | Élevée | Critique | Très haute |
| TC-054 | Vue buy_now vide le panier existant | Élevée | Élevé | Très haute |
| TC-055 | Vue buy_now empêche vendeur d'acheter son produit | Moyenne | Élevé | Haute |
| TC-056 | Vue buy_now refuse quantité invalide | Élevée | Élevé | Très haute |
| TC-057 | Vue generate_invoice_pdf exige authentification | Élevée | Élevé | Très haute |
| TC-058 | Vue generate_invoice_pdf exige sa propre commande | Élevée | Élevé | Très haute |
| TC-059 | Vue generate_invoice_pdf génère un PDF | Élevée | Élevé | Très haute |
| TC-060 | Vue vendor_products exige approbation vendeur | Moyenne | Élevé | Haute |
| TC-061 | Vue vendor_products liste produits du vendeur | Moyenne | Élevé | Haute |
| TC-062 | Vue add_product exige approbation vendeur | Moyenne | Élevé | Haute |
| TC-063 | Vue add_product crée un produit via AJAX | Moyenne | Élevé | Haute |
| TC-064 | Vue add_product affiche le formulaire | Moyenne | Moyen | Moyenne |
| TC-065 | Vue edit_product modifie un produit | Moyenne | Élevé | Haute |
| TC-066 | Vue edit_product limite aux propres produits | Moyenne | Élevé | Haute |
| TC-067 | Vue delete_product supprime un produit | Moyenne | Élevé | Haute |
| TC-068 | Vue vendor_product_detail affiche détails avec stats | Moyenne | Moyen | Moyenne |
| TC-069 | Workflow vendeur complet (création, approbation, produit) | Élevée | Critique | Très haute |
| TC-070 | Vendeur non approuvé ne peut pas accéder | Moyenne | Élevé | Haute |

> **Commentaire priorisation** : l'ordre des risques reflète le cycle utilisateur – modèles et utilitaires (TC-001 à TC-009), panier et checkout (TC-010 à TC-017), tests d'intégration catalogue (TC-018 à TC-025), panier (TC-026 à TC-032), checkout (TC-033 à TC-039), coupons (TC-040 à TC-046), avis (TC-047 à TC-051), achat direct (TC-052 à TC-056), factures (TC-057 à TC-059), vendeur (TC-060 à TC-068), workflow fonctionnel (TC-069 à TC-070). Les priorités « Très haute » couvrent la continuité de revenu (paiement, stock), tandis que les niveaux « Haute/Moyenne » portent sur l'expérience utilisateur.

## 3. Cas de tests détaillés

| ID | Description | Pré-requis | Entrées | Résultat attendu | Résultat obtenu | Statut |
|----|-------------|------------|---------|------------------|----------------|--------|
| TC-001 | Slug catégorie généré automatiquement | Modèle `Category` | Création `Category(name="High Tech")` | slug `high-tech`, `get_absolute_url` fonctionnel | slug créé, URL retournée | ✅ |
| TC-002 | Description produit formatée (Markdown -> HTML) | Produit avec markdown | Appel `formatted_description()` | HTML enrichi avec titres/listes | HTML avec `<h2>` et listes stylées | ✅ |
| TC-003 | Sous-total panier par ligne | Produit en stock | `CartItem(quantity=2)` | `sub_total()` retourne `price*qty` | `sub_total()` calcul exact | ✅ |
| TC-004 | Représentation textuelle d'un avis | Avis existant | `str(review)` | Chaîne `Avis de <user> sur <produit>` | Chaîne conforme | ✅ |
| TC-005 | Validité coupon (actif, date, limites) | Coupons configurés | Appel `is_valid`, `apply_discount`, `calculate_discount` | Résultats cohérents | Booléens et montants attendus | ✅ |
| TC-006 | Coût d'un item de commande | Produit disponible | `OrderItem(price, qty=3)` | `get_cost()` = `price*qty` | Valeur calculée exacte | ✅ |
| TC-007 | Total de commande = somme items | Commande avec items | `Order.get_total_cost()` | Somme exacte des coûts items | Total attendu obtenu | ✅ |
| TC-008 | Réponse HTTP génération facture PDF | Commande + items | `generate_invoice_pdf(order)` | Réponse 200 + PDF en contenu | Statut 200 + données PDF simulées | ✅ |
| TC-009 | Sauvegarde disque de la facture | Commande + items | `save_invoice_pdf(order)` | Fichier `media/invoices/...` créé | Fichier présent dans `media/` | ✅ |
| TC-010 | Ajout panier AJAX renvoie panier mis à jour | Client connecté | POST JSON `{"quantity": 2}` | JSON succès + `total_items=2` | JSON avec `total_items=2` | ✅ |
| TC-011 | Retrait panier décrémente la quantité | Client connecté + panier | POST `/cart/remove/` | JSON succès, quantité décrémentée | JSON succès, compteur décrémenté | ✅ |
| TC-012 | Checkout affiche le récapitulatif | Client avec panier | GET `/shop/checkout` | Contexte contient `total`, `counter`, `cart_items` | Contexte conforme | ✅ |
| TC-013 | Tunnel d'achat complet (checkout -> paiement) | Client, panier, moyen de paiement mocké | Scénario complet `FunctionalCheckoutTests` | Commande créée, stock décrémenté, facture générée | Commande créée, stock réduit, facture générée | ✅ |
| TC-014 | Ajout produit au panier sans authentification | Aucun login | POST AJAX `/shop/cart_add/` | HTTP 401 + message login | Statut 401, message invitant à se connecter | ✅ |
| TC-015 | Produit indisponible refuse l'ajout panier | Produit `stock=0` | POST AJAX | HTTP 400, aucun item créé | Statut 400, panier inchangé | ✅ |
| TC-016 | Quantité > stock refuse l'ajout panier | Produit `stock=2` | POST AJAX qty=5 | HTTP 400, panier inchangé | Statut 400, panier inchangé | ✅ |
| TC-017 | Visiteur redirigé vers login avant checkout | Visiteur | GET `/shop/checkout` | Redirection vers `/login/` | Redirection `302 -> /login/` | ✅ |
| TC-018 | Vue shop liste tous les produits disponibles | Produits en base | GET `/shop/` | Liste produits dans contexte | Produits visibles dans response.context | ✅ |
| TC-019 | Vue shop filtre les produits par catégorie | Catégories et produits | GET `/shop/?category=electronics` | Produits filtrés par catégorie | Seuls produits de la catégorie affichés | ✅ |
| TC-020 | Vue shop recherche des produits par nom | Produits en base | GET `/shop/?search=laptop` | Produits correspondants | Produits avec "laptop" dans le nom | ✅ |
| TC-021 | Vue shop trie les produits (prix, nom, date) | Produits en base | GET `/shop/?sort=price` | Produits triés | Produits ordonnés selon critère | ✅ |
| TC-022 | Vue product_detail affiche les détails d'un produit | Produit disponible | GET `/shop/product/<slug>/` | Détails produit dans contexte | Produit, catégorie, prix visibles | ✅ |
| TC-023 | Vue product_detail affiche les avis du produit | Produit avec avis | GET `/shop/product/<slug>/` | Avis dans contexte | Liste des avis affichée | ✅ |
| TC-024 | Vue product_detail affiche les produits similaires | Produit avec catégorie | GET `/shop/product/<slug>/` | Produits similaires dans contexte | Produits de même catégorie affichés | ✅ |
| TC-025 | Vue product_detail gère les produits indisponibles | Produit `available=False` | GET `/shop/product/<slug>/` | Message indisponible ou 404 | Produit non accessible ou message | ✅ |
| TC-026 | Vue cart_detail affiche un panier vide | Panier sans articles | GET `/shop/cart/` | Panier vide dans contexte | Message panier vide affiché | ✅ |
| TC-027 | Vue cart_detail affiche un panier avec articles | Panier avec items | GET `/shop/cart/` | Articles dans contexte | Liste des articles affichée | ✅ |
| TC-028 | Vue cart_count retourne 0 pour panier vide | Panier sans articles | GET `/shop/cart/count/` | JSON `count=0` | JSON avec count=0 | ✅ |
| TC-029 | Vue cart_count retourne le nombre d'articles | Panier avec items | GET `/shop/cart/count/` | JSON `count=N` | JSON avec count correct | ✅ |
| TC-030 | Vue cart_update augmente la quantité d'un article | Article en panier, stock suffisant | POST `/shop/cart/update/` avec `quantity=3` | Quantité mise à jour | Quantité article = 3 | ✅ |
| TC-031 | Vue cart_update refuse quantité > stock | Article en panier, stock=2 | POST avec `quantity=5` | Quantité inchangée | Quantité reste à valeur initiale | ✅ |
| TC-032 | Vue delete_from_cart supprime un article | Article en panier | POST `/shop/cart/delete/<item_id>/` | Article supprimé | Article absent du panier | ✅ |
| TC-033 | Vue checkout exige une authentification | Visiteur non connecté | GET `/shop/checkout/` | Redirection `/login/` | Redirection 302 vers login | ✅ |
| TC-034 | Vue checkout affiche le récapitulatif avec articles | Client connecté, panier avec items | GET `/shop/checkout/` | Total, compteur, items dans contexte | Récapitulatif complet affiché | ✅ |
| TC-035 | Vue checkout gère un panier vide | Client connecté, panier vide | GET `/shop/checkout/` | Message ou redirection | Message panier vide ou redirection | ✅ |
| TC-036 | Vue process_payment crée une commande | Client connecté, panier avec items | POST `/shop/process-payment/` avec données | Commande créée en base | Order créé avec items | ✅ |
| TC-037 | Vue process_payment met à jour le stock | Produits en panier | POST `/shop/process-payment/` | Stock décrémenté | Stock réduit de quantité achetée | ✅ |
| TC-038 | Vue payment_success affiche succès avec commande | Commande existante | GET `/shop/payment-success/?order_id=X` | Page succès avec commande | Commande affichée | ✅ |
| TC-039 | Vue payment_success gère l'absence de commande | Aucune commande | GET `/shop/payment-success/` | Message ou redirection | Message erreur ou redirection | ✅ |
| TC-040 | Vue apply_coupon applique un coupon valide | Coupon valide, panier avec montant suffisant | POST `/shop/apply-coupon/` avec code | Coupon appliqué en session | Réduction calculée | ✅ |
| TC-041 | Vue apply_coupon refuse un coupon invalide | Code coupon inexistant | POST avec code invalide | Message erreur | Message "coupon invalide" | ✅ |
| TC-042 | Vue apply_coupon refuse montant minimum non atteint | Coupon avec min_purchase, panier insuffisant | POST avec code | Message erreur | Message "montant minimum non atteint" | ✅ |
| TC-043 | Vue remove_coupon supprime le coupon appliqué | Coupon appliqué en session | POST `/shop/remove-coupon/` | Coupon retiré de session | Session sans coupon | ✅ |
| TC-044 | Vue validate_coupon_ajax valide un coupon valide | Coupon valide | POST AJAX avec code | JSON `valid=True` | JSON succès avec validité | ✅ |
| TC-045 | Vue validate_coupon_ajax refuse un coupon invalide | Code invalide | POST AJAX avec code invalide | JSON `valid=False` | JSON erreur | ✅ |
| TC-046 | Vue validate_coupon_ajax refuse un coupon expiré | Coupon expiré | POST AJAX avec code expiré | JSON `valid=False` | JSON erreur expiration | ✅ |
| TC-047 | Vue add_review exige une authentification | Visiteur non connecté | POST `/shop/add-review/<product_id>/` | Redirection `/login/` | Redirection 302 | ✅ |
| TC-048 | Vue add_review ajoute un avis via AJAX | Client connecté, produit disponible | POST AJAX avec titre/note/commentaire | Avis créé en base | Review créé avec données | ✅ |
| TC-049 | Vue add_review met à jour un avis existant | Avis existant du même utilisateur | POST AJAX avec nouvelles données | Avis mis à jour | Review modifié | ✅ |
| TC-050 | Vue add_review refuse une note invalide | Note < 1 ou > 5 | POST AJAX avec note=6 | Message erreur | JSON erreur validation | ✅ |
| TC-051 | Vue add_review refuse un titre vide | Titre vide | POST AJAX avec titre="" | Message erreur | JSON erreur validation | ✅ |
| TC-052 | Vue buy_now exige une authentification | Visiteur non connecté | POST `/shop/buy-now/<product_id>/` | Redirection `/login/` | Redirection 302 | ✅ |
| TC-053 | Vue buy_now crée un panier et redirige | Client connecté, produit disponible | POST avec `quantity=1` | Panier créé, redirection checkout | Redirection 302 vers checkout | ✅ |
| TC-054 | Vue buy_now vide le panier existant | Panier avec articles existants | POST buy_now pour nouveau produit | Ancien panier vidé, nouveau produit ajouté | Seul nouveau produit en panier | ✅ |
| TC-055 | Vue buy_now empêche vendeur d'acheter son produit | Vendeur connecté, son propre produit | POST buy_now pour son produit | Message erreur ou redirection | Accès refusé | ✅ |
| TC-056 | Vue buy_now refuse quantité invalide | Quantité <= 0 ou > stock | POST avec `quantity=0` | Message erreur | JSON erreur validation | ✅ |
| TC-057 | Vue generate_invoice_pdf exige authentification | Visiteur non connecté | GET `/shop/invoice/<order_id>/pdf/` | Redirection `/login/` | Redirection 302 | ✅ |
| TC-058 | Vue generate_invoice_pdf exige sa propre commande | Client connecté, commande d'un autre | GET avec order_id d'un autre | Message erreur ou 404 | Accès refusé | ✅ |
| TC-059 | Vue generate_invoice_pdf génère un PDF | Client connecté, sa propre commande | GET avec order_id valide | Réponse PDF 200 | PDF généré avec données commande | ✅ |
| TC-060 | Vue vendor_products exige approbation vendeur | Vendeur non approuvé | GET `/shop/vendor/products/` | Redirection `/profile/` | Redirection avec message | ✅ |
| TC-061 | Vue vendor_products liste produits du vendeur | Vendeur approuvé | GET `/shop/vendor/products/` | Produits du vendeur dans contexte | Seuls produits du vendeur affichés | ✅ |
| TC-062 | Vue add_product exige approbation vendeur | Vendeur non approuvé | POST `/shop/add_product/` | Redirection `/profile/` | Redirection avec message | ✅ |
| TC-063 | Vue add_product crée un produit via AJAX | Vendeur approuvé | POST AJAX avec données produit | Produit créé en base | Product créé lié au vendeur | ✅ |
| TC-064 | Vue add_product affiche le formulaire | Vendeur approuvé | GET `/shop/add_product/` | Formulaire dans contexte | Formulaire affiché | ✅ |
| TC-065 | Vue edit_product modifie un produit | Vendeur approuvé, son produit | POST `/shop/edit_product/<id>/` avec nouvelles données | Produit mis à jour | Champs modifiés en base | ✅ |
| TC-066 | Vue edit_product limite aux propres produits | Vendeur approuvé, produit d'un autre | POST edit_product pour produit autre | Message erreur ou 404 | Accès refusé | ✅ |
| TC-067 | Vue delete_product supprime un produit | Vendeur approuvé, son produit | POST `/shop/vendor/product/<id>/delete/` | Produit supprimé | Product supprimé de la base | ✅ |
| TC-068 | Vue vendor_product_detail affiche détails avec stats | Vendeur approuvé, son produit | GET `/shop/vendor/product/<id>/` | Détails + statistiques ventes | Produit et stats affichés | ✅ |
| TC-069 | Workflow vendeur complet (création, approbation, produit) | Utilisateur standard | Scénario complet : demande → approbation → ajout produit | Vendeur créé, approuvé, produit ajouté | Toutes étapes réussies | ✅ |
| TC-070 | Vendeur non approuvé ne peut pas accéder | Vendeur non approuvé | Tentative accès dashboard | Redirection `/profile/` | Accès refusé avec message | ✅ |

> **Commentaire cas de tests** : chaque ID correspond aux 73 tests exécutés dans `Hackerz_E_commerce/tests/`. L'ordre suit le parcours logique : modèles et utilitaires (TC-001 à TC-009), panier et checkout de base (TC-010 à TC-017), tests d'intégration catalogue (TC-018 à TC-025), panier (TC-026 à TC-032), checkout (TC-033 à TC-039), coupons (TC-040 à TC-046), avis (TC-047 à TC-051), achat direct (TC-052 à TC-056), factures (TC-057 à TC-059), vendeur (TC-060 à TC-068), workflow fonctionnel (TC-069 à TC-070). La colonne « Statut » confirme l'exécution réussie via `pytest -vv --cov=.`, garantissant la traçabilité entre scénario priorisé et validation automatisée.

## 4. Correspondance tests / fonctionnalités

### 4.1 Modèles & Utilitaires

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_models.py::CategoryModelTests.test_slug_is_automatically_generated` | TC-001 – Génération slug catégorie |
| `Hackerz_E_commerce/tests/test_models.py::ProductModelTests.test_formatted_description_enriches_markdown` | TC-002 – Markdown produit enrichi |
| `Hackerz_E_commerce/tests/test_models.py::CartModelTests.test_cart_item_subtotal` | TC-003 – Sous-total ligne panier |
| `Hackerz_E_commerce/tests/test_models.py::ReviewModelTests.test_review_string_representation` | TC-004 – Représentation avis |
| `Hackerz_E_commerce/tests/test_models.py::CouponModelTests.*` | TC-005 – Règles coupons |
| `Hackerz_E_commerce/tests/test_models.py::OrderModelTests.test_order_item_cost` | TC-006 – Coût ligne commande |
| `Hackerz_E_commerce/tests/test_models.py::OrderModelTests.test_order_total_cost_is_sum_of_items` | TC-007 – Total commande |
| `Hackerz_E_commerce/tests/test_utils.py::InvoiceUtilsTests.test_generate_invoice_pdf_returns_response` | TC-008 – Réponse HTTP facture |
| `Hackerz_E_commerce/tests/test_utils.py::InvoiceUtilsTests.test_save_invoice_pdf_creates_file` | TC-009 – Sauvegarde facture |

### 4.2 Panier & Checkout de base

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_cart_add_creates_cart_item` | TC-010 – Ajout panier AJAX succès |
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_cart_remove_decrements_quantity` | TC-011 – Retrait panier |
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_checkout_context_contains_cart_summary` | TC-012 – Contexte checkout |
| `Hackerz_E_commerce/tests/test_functional_checkout.py::FunctionalCheckoutTests.test_customer_can_complete_checkout_flow` | TC-013 – Parcours commande complet |
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_cart_add_requires_authentication` | TC-014 – Authentification requise |
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_cart_add_fails_when_product_out_of_stock` | TC-015 – Produit indisponible |
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_cart_add_fails_when_quantity_exceeds_stock` | TC-016 – Quantité > stock |
| `Hackerz_E_commerce/tests/test_views.py::CartViewsTests.test_checkout_requires_login` | TC-017 – Checkout protège visiteur |

### 4.3 Tests d'intégration - Catalogue

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestShopView.test_shop_view_lists_products` | TC-018 – Liste des produits disponibles |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestShopView.test_shop_view_filters_by_category` | TC-019 – Filtrage par catégorie |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestShopView.test_shop_view_search` | TC-020 – Recherche de produits |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestShopView.test_shop_view_sorting` | TC-021 – Tri des produits |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestProductDetailView.test_product_detail_view` | TC-022 – Détails d'un produit |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestProductDetailView.test_product_detail_shows_reviews` | TC-023 – Affichage des avis sur le produit |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestProductDetailView.test_product_detail_shows_related_products` | TC-024 – Produits similaires |
| `Hackerz_E_commerce/tests/test_integration_shop.py::TestProductDetailView.test_product_detail_unavailable_product` | TC-025 – Produit indisponible |

### 4.4 Tests d'intégration - Panier

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestCartDetailView.test_cart_detail_view_empty` | TC-026 – Affichage panier vide |
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestCartDetailView.test_cart_detail_view_with_items` | TC-027 – Affichage panier avec articles |
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestCartCountView.test_cart_count_empty` | TC-028 – Compteur panier vide |
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestCartCountView.test_cart_count_with_items` | TC-029 – Compteur panier avec articles |
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestCartUpdateView.test_cart_update_increases_quantity` | TC-030 – Mise à jour quantité panier |
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestCartUpdateView.test_cart_update_exceeds_stock` | TC-031 – Mise à jour quantité > stock |
| `Hackerz_E_commerce/tests/test_integration_cart.py::TestDeleteFromCartView.test_delete_from_cart` | TC-032 – Suppression d'un article du panier |

### 4.5 Tests d'intégration - Checkout & Paiement

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestCheckoutView.test_checkout_requires_login` | TC-033 – Checkout exige authentification |
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestCheckoutView.test_checkout_with_items` | TC-034 – Checkout avec articles |
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestCheckoutView.test_checkout_empty_cart` | TC-035 – Checkout panier vide |
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestProcessPaymentView.test_process_payment_creates_order` | TC-036 – Création commande lors du paiement |
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestProcessPaymentView.test_process_payment_updates_stock` | TC-037 – Mise à jour stock lors du paiement |
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestPaymentSuccessView.test_payment_success_with_order` | TC-038 – Succès paiement avec commande |
| `Hackerz_E_commerce/tests/test_integration_checkout.py::TestPaymentSuccessView.test_payment_success_without_order` | TC-039 – Succès paiement sans commande |

### 4.6 Tests d'intégration - Coupons

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestApplyCouponView.test_apply_coupon_valid` | TC-040 – Application coupon valide |
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestApplyCouponView.test_apply_coupon_invalid_code` | TC-041 – Application coupon invalide |
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestApplyCouponView.test_apply_coupon_min_purchase_not_met` | TC-042 – Application coupon montant minimum non atteint |
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestRemoveCouponView.test_remove_coupon` | TC-043 – Suppression coupon |
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestValidateCouponAjaxView.test_validate_coupon_ajax_valid` | TC-044 – Validation AJAX coupon valide |
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestValidateCouponAjaxView.test_validate_coupon_ajax_invalid` | TC-045 – Validation AJAX coupon invalide |
| `Hackerz_E_commerce/tests/test_integration_coupon.py::TestValidateCouponAjaxView.test_validate_coupon_ajax_expired` | TC-046 – Validation AJAX coupon expiré |

### 4.7 Tests d'intégration - Avis produits

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_reviews.py::TestAddReviewView.test_add_review_requires_login` | TC-047 – Ajout avis exige authentification |
| `Hackerz_E_commerce/tests/test_integration_reviews.py::TestAddReviewView.test_add_review_ajax` | TC-048 – Ajout avis via AJAX |
| `Hackerz_E_commerce/tests/test_integration_reviews.py::TestAddReviewView.test_add_review_updates_existing` | TC-049 – Mise à jour avis existant |
| `Hackerz_E_commerce/tests/test_integration_reviews.py::TestAddReviewView.test_add_review_invalid_rating` | TC-050 – Ajout avis note invalide |
| `Hackerz_E_commerce/tests/test_integration_reviews.py::TestAddReviewView.test_add_review_empty_title` | TC-051 – Ajout avis titre vide |

### 4.8 Tests d'intégration - Achat direct

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_buy_now.py::TestBuyNowView.test_buy_now_requires_login` | TC-052 – Achat direct exige authentification |
| `Hackerz_E_commerce/tests/test_integration_buy_now.py::TestBuyNowView.test_buy_now_creates_cart_and_redirects` | TC-053 – Achat direct crée panier et redirige |
| `Hackerz_E_commerce/tests/test_integration_buy_now.py::TestBuyNowView.test_buy_now_clears_existing_cart` | TC-054 – Achat direct vide panier existant |
| `Hackerz_E_commerce/tests/test_integration_buy_now.py::TestBuyNowView.test_buy_now_vendor_cannot_buy_own_product` | TC-055 – Vendeur ne peut pas acheter son propre produit |
| `Hackerz_E_commerce/tests/test_integration_buy_now.py::TestBuyNowView.test_buy_now_invalid_quantity` | TC-056 – Achat direct quantité invalide |

### 4.9 Tests d'intégration - Factures

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_invoice.py::TestGenerateInvoicePdfView.test_generate_invoice_pdf_requires_login` | TC-057 – Génération facture exige authentification |
| `Hackerz_E_commerce/tests/test_integration_invoice.py::TestGenerateInvoicePdfView.test_generate_invoice_pdf_requires_own_order` | TC-058 – Génération facture exige sa propre commande |
| `Hackerz_E_commerce/tests/test_integration_invoice.py::TestGenerateInvoicePdfView.test_generate_invoice_pdf_success` | TC-059 – Génération facture PDF succès |

### 4.10 Tests d'intégration - Vendeur

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestVendorProductsView.test_vendor_products_requires_approval` | TC-060 – Dashboard vendeur exige approbation |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestVendorProductsView.test_vendor_products_lists_own_products` | TC-061 – Dashboard liste produits du vendeur |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestAddProductView.test_add_product_requires_approval` | TC-062 – Ajout produit exige approbation |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestAddProductView.test_add_product_ajax` | TC-063 – Ajout produit via AJAX |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestAddProductView.test_add_product_get_form` | TC-064 – Formulaire ajout produit |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestEditProductView.test_edit_product` | TC-065 – Modification produit |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestEditProductView.test_edit_product_only_own_products` | TC-066 – Modification uniquement ses propres produits |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestDeleteProductView.test_delete_product` | TC-067 – Suppression produit |
| `Hackerz_E_commerce/tests/test_integration_vendor.py::TestVendorProductDetailView.test_vendor_product_detail` | TC-068 – Détails produit vendeur avec statistiques |

### 4.11 Tests fonctionnels - Vendeur

| Test (fichier::fonction) | Fonctionnalité couverte |
|--------------------------|-------------------------|
| `Hackerz_E_commerce/tests/test_functional_vendor_workflow.py::TestVendorWorkflow.test_complete_vendor_workflow` | TC-069 – Workflow vendeur complet (création, approbation, ajout produit) |
| `Hackerz_E_commerce/tests/test_functional_vendor_workflow.py::TestVendorWorkflow.test_vendor_cannot_access_without_approval` | TC-070 – Vendeur non approuvé ne peut pas accéder |


## 5. Rapport Flake8

| Chemin | Type | Motif | Remarques |
|--------|------|-------|-----------|
| `flake8` global | Échec | ~2 600+ avertissements (lignes >79, espaces, imports inutiles) | Résultats dominés par les fichiers du projet et du dossier `api/`. |
| `Hackerz/views.py` | E501, W293, F541, etc. | Nombreuses lignes trop longues (>79), espaces fin de ligne, try/except nus, f-string incomplet | Fichier très volumineux (>1 000 lignes). Refactoriser par vues spécialisées, appliquer formatage auto (black/isort). |
| `Hackerz_blog/views.py` | E501, F821, F841, W293 | Plus de 200 lignes signalées, variables non définies (`slugify`), imports inutilisés | Introduire `slugify`, nettoyer imports/méthodes, envisager tests pour prévenir régressions. |
| `Hackerz_E_commerce/models.py` | E501, W293 | Définitions de modèles avec lignes >79, espaces inutiles | Possible application de `black`/`ruff` et découpe des chaînes. |
| `api/api_test.py` | E501, W293, F541, etc. | Script long, non formaté, import ombré (`requests`) | Script manuel → soit retrait du rapport, soit nettoyage via formatter. |
| Autres (`serializers.py`, `urls.py`, `management/`, etc.) | E501, W293, F401 | Lignes longues, imports inutiles, absence de newline final | Formatage automatique recommandé. |

## 6. Résultats d'exécution
- **Commande** : `python -m pytest Hackerz_E_commerce/tests/ -v --cov=Hackerz_E_commerce --cov-report=term-missing`
- **Résultat** : `======================= 73 passed, 2 warnings in 44.83s =======================`
- **Environnement** : Python 3.10, Django 5.0.1, SQLite, backend mail mémoire, DRF `APIClient`.
- **Commandes complémentaires** :
  - Exécution simple : `python -m pytest Hackerz_E_commerce/tests/ -v`
  - Exécution avec couverture : `python -m pytest Hackerz_E_commerce/tests/ -v --cov=Hackerz_E_commerce --cov-report=term-missing`
  - Lancement ciblé (exemple) : `python -m pytest Hackerz_E_commerce/tests/test_integration_shop.py -v`
  - Rapport Flake8 : `python -m flake8 --exclude=.venv,venv`
  - Nettoyage/initialisation BDD (si besoin) : `python manage.py migrate`

## 7. Rapport de couverture
- **Couverture globale** : 86 % (2 007 instructions, 284 non couvertes).
- **Points forts** : Tests fonctionnels et d'intégration `Hackerz_E_commerce/tests/*` à 100 % pour la plupart des fichiers ; modèles e-commerce à 98 % ; utilitaires à 95 % ; formulaires et admin e-commerce à 100 %.
- **Axes d'amélioration** : vues `Hackerz_E_commerce/views.py` (63 %), `Hackerz_E_commerce/views_coupon.py` (67 %), modules back-office hors périmètre e-commerce (`Hackerz/admin.py`, `api/*.py`) encore non couverts.
- **Livrables** : console `term-missing` listant les lignes manquantes.

### 7.2 Tableau de couverture par module

| Module | Couverture | Statut | Observations |
|--------|-----------|--------|---------------|
| **Tests** | | | |
| `Hackerz_E_commerce/tests/test_models.py` | 100 % | ✅ Excellent | Modèles e-commerce entièrement testés |
| `Hackerz_E_commerce/tests/test_utils.py` | 100 % | ✅ Excellent | Utilitaires PDF entièrement testés |
| `Hackerz_E_commerce/tests/test_views.py` | 100 % | ✅ Excellent | Vues panier/checkout entièrement testées |
| `Hackerz_E_commerce/tests/test_functional_checkout.py` | 100 % | ✅ Excellent | Tunnel d'achat complet validé |
| `Hackerz_E_commerce/tests/test_functional_vendor_workflow.py` | 100 % | ✅ Excellent | Workflow vendeur complet validé |
| `Hackerz_E_commerce/tests/test_integration_shop.py` | 97 % | ✅ Excellent | Tests d'intégration catalogue/produits |
| `Hackerz_E_commerce/tests/test_integration_cart.py` | 100 % | ✅ Excellent | Tests d'intégration panier |
| `Hackerz_E_commerce/tests/test_integration_checkout.py` | 100 % | ✅ Excellent | Tests d'intégration checkout/paiement |
| `Hackerz_E_commerce/tests/test_integration_vendor.py` | 100 % | ✅ Excellent | Tests d'intégration vendeur |
| `Hackerz_E_commerce/tests/test_integration_coupon.py` | 100 % | ✅ Excellent | Tests d'intégration coupons |
| `Hackerz_E_commerce/tests/test_integration_reviews.py` | 100 % | ✅ Excellent | Tests d'intégration avis |
| `Hackerz_E_commerce/tests/test_integration_buy_now.py` | 94 % | ✅ Excellent | Tests d'intégration achat direct |
| `Hackerz_E_commerce/tests/test_integration_invoice.py` | 100 % | ✅ Excellent | Tests d'intégration factures |
| **Application principale** | | | |
| `Hackerz_E_commerce/models.py` | 98 % | ✅ Excellent | Modèles bien testés |
| `Hackerz_E_commerce/views.py` | 63 % | ✅ Bon | Vues e-commerce majoritairement testées |
| `Hackerz_E_commerce/views_coupon.py` | 67 % | ✅ Bon | Vues coupons partiellement testées |
| `Hackerz_E_commerce/utils.py` | 95 % | ✅ Excellent | Utilitaires entièrement testés |
| `Hackerz_E_commerce/forms.py` | 100 % | ✅ Excellent | Formulaires entièrement testés |
| `Hackerz_E_commerce/admin.py` | 100 % | ✅ Excellent | Configuration admin testée |

### 7.3 Analyse de la couverture

**Points forts** :
- Tests fonctionnels et d'intégration (`Hackerz_E_commerce/tests/*`) à 100 % pour la plupart des fichiers
- Modèles e-commerce à 98 %
- Utilitaires PDF à 95 %
- Formulaires e-commerce à 100 %
- Configuration admin e-commerce à 100 %
- Tests organisés en unitaires, intégration et fonctionnels

**Axes d'amélioration** :
- Vues `Hackerz_E_commerce/views.py` (63 %) : certaines vues de catalogue et de produits nécessitent des tests supplémentaires
- Vues coupons `Hackerz_E_commerce/views_coupon.py` (67 %) : quelques cas limites non couverts

## 8. Couverture par type
- **Unitaires** : modèles e-commerce (`test_models.py`), utilitaires PDF (`test_utils.py`), vues panier de base (`test_views.py`).
- **Intégration** : 
  - Catalogue et produits (`test_integration_shop.py`) : 8 tests
  - Panier (`test_integration_cart.py`) : 7 tests
  - Checkout et paiement (`test_integration_checkout.py`) : 7 tests
  - Vendeur (`test_integration_vendor.py`) : 9 tests
  - Coupons (`test_integration_coupon.py`) : 7 tests
  - Avis produits (`test_integration_reviews.py`) : 5 tests
  - Achat direct (`test_integration_buy_now.py`) : 5 tests
  - Factures PDF (`test_integration_invoice.py`) : 3 tests
- **Fonctionnels** : 
  - Tunnel d'achat complet (`test_functional_checkout.py`) : 1 test
  - Workflow vendeur complet (`test_functional_vendor_workflow.py`) : 2 tests

---
