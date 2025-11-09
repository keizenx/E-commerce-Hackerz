# Rapport de tests – Hackerz E-commerce

## 1. Plan de test
- **Objectif** : Garantir les parcours essentiels d’un site e-commerce multirôle (visiteur, client, vendeur, administrateur) avant d’étendre les spécifications.
- **Périmètre** : gestion des produits, panier/checkout, coupons, facturation PDF, comptes utilisateurs et gouvernance admin.
- **Outils** : `pytest`, `pytest-django`, client de test Django, doubles (mock) pour l’emailing et la génération PDF.
- **Commande de référence** (affiche chaque test) :
  ```bash
  pytest -vv
  ```
- **Critères de succès** :
  - 100 % des tests critiques “checkout / paiement” passent.
  - Pas de régression sur l’intégrité des données (stock, total, coupons).
  - Les rôles clés disposent bien de leurs permissions.

## 2. Matrice de risque / priorisation

Fonctionnalité / scénario testé                                       | Probabilité | Impact   | Priorité |
----------------------------------------------------------------------|-------------|----------|----------|
Génération automatique du slug catégorie (`CategoryModelTests`)       | Moyenne     | Moyen    | Moyenne  |
Formatage Markdown produit (`ProductModelTests`)                      | Moyenne     | Moyen    | Moyenne  |
Calcul du total de commande (`OrderModelTests`)                       | Élevée      | Critique | Très haute |
Validation des coupons (`CouponModelTests`)                           | Moyenne     | Élevé    | Haute    |
Sauvegarde facture PDF (`InvoiceUtilsTests`)                          | Moyenne     | Élevé    | Haute    |
Réponse HTTP PDF générée (`InvoiceUtilsTests`)                        | Moyenne     | Élevé    | Haute    |
Ajout panier via AJAX (`CartViewsTests`)                              | Élevée      | Élevé    | Très haute |
Visiteur redirigé vers login avant commande (`CartViewsTests`)        | Élevée      | Critique | Très haute |
Utilisateur complète la commande (`FunctionalCheckoutTests`)          | Élevée      | Critique | Très haute |
Vendeur approuvé crée un produit (`test_authorised_vendor_can_create_product`) | Moyenne | Élevé | Haute |
Tableau de bord vendeur liste ses produits (`test_vendor_dashboard_lists_their_products`) | Moyenne | Moyen | Moyenne |
Inscription visiteur : compte inactif (`test_visitor_registration_creates_inactive_account`) | Élevée | Élevé | Très haute |
Admin approuve un vendeur (`test_admin_can_approve_vendor`)           | Moyenne     | Élevé    | Haute    |
Notification email demande vendeur (`test_vendor_request_sends_notification_email`) | Moyenne | Élevé | Haute |
Client authentifié ajoute un produit au panier (`test_authenticated_customer_can_add_products_to_cart`) | Élevée | Élevé | Très haute |

## 3. Cas de test détaillés

| ID     | Description                                         | Pré-requis                                   | Entrées                                                  | Résultat attendu                                                                 | Statut |
|--------|-----------------------------------------------------|-----------------------------------------------|----------------------------------------------------------|----------------------------------------------------------------------------------|--------|
| TC-001 | Génération du slug & URL catégorie                  | Base de données initialisée                   | `Category(name="High Tech")`                             | Slug `high-tech`, `get_absolute_url()` valide                                    | ✅     |
| TC-002 | Formatage Markdown produit                          | Catégorie existante                           | Description Markdown                                     | HTML contenant `<h2>` et bloc code enrichi                                      | ✅     |
| TC-003 | Calcul total commande                               | Produit en stock                              | `OrderItem` (qty 2 + 1)                                  | `order.get_total_cost()` retourne la somme exacte                               | ✅     |
| TC-004 | Validation coupon (dates, usage, montant)           | Coupon actif                                  | Total 200 €, type pourcentage & montant fixe              | Réduction plafonnée, invalidation si date/pavage dépassé                        | ✅     |
| TC-005 | Sauvegarde facture PDF                              | Commande avec items                           | `save_invoice_pdf(order)`                                | Fichier `media/invoices/facture_<id>.pdf` généré                                | ✅     |
| TC-006 | Génération réponse PDF                              | Commande avec items                           | `generate_invoice_pdf(order)`                            | Réponse HTTP 200 avec PDF en contenu                                            | ✅     |
| TC-007 | Ajout panier AJAX (client authentifié)              | Utilisateur connecté, produit disponible      | POST `/shop/cart/add/<id>` (qty 2)                       | JSON succès, `total_items == 2`                                                 | ✅     |
| TC-008 | Checkout nécessite connexion                        | Aucun compte connecté                         | GET `/shop/checkout`                                     | Redirection vers `/login/`                                                      | ✅     |
| TC-009 | Parcours checkout complet                           | Client connecté, panier plein                 | POST `/shop/process_payment` (coordonnées)               | Commande payée, stock décrémenté, email simulé, redirection succès              | ✅     |
| TC-010 | Création produit par vendeur approuvé               | Utilisateur vendeur approuvé, catégorie       | POST AJAX `/shop/vendor/product/add/` + image            | JSON succès, produit associé au vendeur créé                                    | ✅     |
| TC-011 | Tableau de bord vendeur liste ses produits          | Produit appartenant au vendeur                | GET `/shop/vendor/products/`                             | Réponse 200, produit présent dans le contexte                                   | ✅     |
| TC-012 | Inscription visiteur crée compte inactif            | Formulaire d’inscription accessible           | POST `/register` (credentials valides)                   | Utilisateur créé `is_active=False`, redirection confirmation                    | ✅     |
| TC-013 | Admin peut approuver un vendeur                     | Superuser connecté, vendor non approuvé       | GET `/admin/Hackerz/vendor/<id>/approve/`                | Vendor `is_approved=True`, succès sans envoi réel d’email (mock)                | ✅     |
| TC-014 | Notification email lors de la demande vendeur       | Utilisateur connecté non-vendeur              | POST `/become-vendor/` + justificatif identité           | `profile.is_vendor=True`, email envoyé à l’administrateur                       | ✅     |

## 4. Résultats d’exécution
- **Commande** : `pytest -vv`
- **Sortie attendue** : affichage de chaque test (ex. `tests/test_user_roles.py::test_authorised_vendor_can_create_product PASSED`)
- **Synthèse** : 25 tests passés sur 25 + 1 test externe ignoré (`================= 25 passed, 1 skipped in ~11s =================`)  
- **Environnement** : Windows 10, Python 3.10, Django 5.0.1, base SQLite, backend email mémoire/mock.

## 5. Couverture par type
- **Unitaires** : `Hackerz_E_commerce/tests/test_models.py`, `test_utils.py` – logique métier (prix, coupons, PDF).
- **Intégration** : `Hackerz_E_commerce/tests/test_views.py` – panier & checkout, règles de sessions/API.
- **Fonctionnels** : `Hackerz_E_commerce/tests/test_functional_checkout.py`, `tests/test_user_roles.py`, `tests/test_vendor_onboarding.py` – scénarios bout-en-bout (vente, inscription, administration, notifications).

## 6. Importance métier
- **Vendeur** : vérification que seuls les vendeurs approuvés gèrent leur catalogue et que l’admin conserve la main.
- **Client / visiteur** : parcours d’inscription et conversion sécurisés, obligations de compte avant paiement.
- **Finance** : factures PDF et coupons validés évitent écarts comptables.
- **Gouvernance** : couverture admin garantit que l’équipe peut approuver/rejeter les vendeurs sans régression.

## 7. Recommandations
- Étendre la couverture aux API REST (Swagger), wishlist et coupons via session.
- Ajouter des scénarios échec (ex. paiement refusé, vendor non approuvé) pour enrichir la matrice de risques.
- Brancher `coverage.py` et publier le rapport dans la CI.
- Documenter des tests manuels complémentaires (responsive, accessibilité).

---
Rapport généré automatiquement le `08/11/2025`.

