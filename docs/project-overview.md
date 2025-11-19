# Projet Django Hackerz E-Commerce – Document de synthèse

## 1. Contexte et objectifs
- **Nom du projet :** Django Hackerz E-Commerce & Blog
- **Enjeux :**
  - Plateforme e-commerce multi-rôles (visiteur, client, vendeur, administrateur).
  - Gestion complète des produits, commandes, coupons, facturation PDF, profils utilisateurs.
  - Intégration blog + API REST (Swagger) pour contenus marketing et services externes.
- **Objectifs principaux :**
  - Garantir un tunnel d’achat fiable et sécurisé.
  - Permettre aux vendeurs approuvés de gérer leur catalogue.
  - Assurer la gouvernance admin (approbations, notifications, supervision).
  - Maintenir l’intégrité des données financières (stocks, coupons, factures).

## 2. Architecture et composants clés
### 2.1 Applications Django
| App | Rôle principal |
|-----|----------------|
| `Hackerz` | Authentification, profils, vendors, newsletter, vues transverses |
| `Hackerz_E_commerce` | Produits, catégories, panier, commandes, coupons, factures |
| `api` | Endpoints REST (catalogue, blog, authentification) |

tests/
  ├─ test_user_roles.py             # scénarios fonctionnels transverses (clients, vendeurs, admin)
  └─ test_vendor_onboarding.py      # demande vendeur + notification email

Hackerz_E_commerce/tests/
  ├─ __init__.py
  ├─ test_functional_checkout.py    # parcours complet panier → paiement → facture/email
  ├─ test_models.py                 # modèles catalogue/commande/coupon/cart/review
  ├─ test_utils.py                  # utilitaires PDF (generate/save invoice)
  └─ test_views.py                  # vues panier/checkout (AJAX, redirections, contexte)

### 2.2 Technologies
- **Back-end :** Django 5.0.1, DRF, SQLite (dev), Jazzmin (admin UI).
- **Front-end :** Templates HTML/CSS/JS, Bootstrap.
- **Tests :** `pytest`, `pytest-django`, `locmem` email backend, mocks.
- **Services externes :** SMTP Gmail (prod – à injecter via secrets), `xhtml2pdf` pour factures.

### 2.3 Flux critiques
1. **Visiteur → Client :** inscription (compte inactif jusqu’à confirmation email), connexion obligatoire avant paiement.
2. **Client → Commande :**
   - Panier AJAX, gestion des quantités, coupons.
   - Checkout + Process_payment → création commande, décrément stock, facture PDF, email confirmation.
3. **Vendeur :**
   - Formulaire “devenir vendeur” avec justificatif (PDF), notification admin.
   - Tableau de bord vendeur, CRUD produits, statistiques.
4. **Administrateur :**
   - Approber/rejeter les vendeurs, actions email, gestion catalogue globale.

## 3. Qualité logicielle et stratégie de tests
### 3.1 Plan de test (extraits)
- Priorité sur le tunnel d’achat, les notifications critiques, l’intégrité des données et la gouvernance admin.
- Utilisation de fixtures `pytest` (`conftest.py`) pour créer utilisateurs/vendeurs/produits temporaires, et ignorant les scripts manuels (`collect_ignore`).
- Backend email local (`locmem`) et mocks PDF pour vérifier les notifications et factures.

### 3.2 Résultats
- Commande : `pytest -vv`
- Résumé : `26 passed` (aucun test ignoré). Durée ~20 s sur Windows 10, Python 3.10.

### 3.3 Cas de tests fonctionnels majeurs
| ID | Scénario | Statut |
|----|----------|--------|
| TC-017 | Parcours complet de commande (panier → paiement → email) | ✅ |
| TC-015 | Redirection d’un visiteur vers login avant checkout | ✅ |
| TC-018 | Création produit par vendeur approuvé (AJAX + image) | ✅ |
| TC-024 | Notification email lors d’une demande vendeur | ✅ |
| TC-023 | Approbation d’un vendeur depuis l’admin | ✅ |
| TC-020 | Inscription visiteur → compte inactif en attente de confirmation | ✅ |
| TC-026 | Refus d’inscription avec email/username dupliqués | ✅ |

## 4. Analyse de risques et priorisation
| Fonctionnalité / test | Probabilité | Impact | Priorité | Mitigation |
|------------------------|-------------|--------|----------|-----------|
| Process_payment & factures | Élevée | Critique | Très haute | Tests fonctionnels + mocks SMTP/PDF |
| Authentification & redirection login | Élevée | Critique | Très haute | `CartViewsTests.test_checkout_requires_login`, `test_guest_is_redirected_to_login_before_checkout` |
| Coupons (modèle) | Moyenne | Élevé | Haute | `CouponModelTests` (validité, limites) |
| Panier AJAX & flux panier | Élevée | Élevé | Très haute | `CartViewsTests` (add/remove/update) |
| Vendeur : création produits / notifications | Moyenne | Élevé | Haute | `test_authorised_vendor_can_create_product`, `test_vendor_request_sends_notification_email` |
| Admin : approbation vendeur | Moyenne | Élevé | Haute | `test_admin_can_approve_vendor` |

## 5. Recommandations et chantiers à venir
1. **Scénarios d’échec** : couvrir paiements refusés, vendeur rejeté, erreurs coupons et logs notifications.
2. **Tests REST complémentaires** : réintroduire des tests API (produits/blog) lorsque l’interface sera stable.
3. **Automatisation CI/CD** : intégrer `pytest` + `coverage.py` dans un pipeline (GitHub Actions / GitLab CI).
4. **Observabilité** : journaliser les envois email et surveiller les erreurs SMTP.
5. **Sécurité & conformité** : audits CSRF, RGPD (gestion des données personnelles, anonymisation).
6. **Performance** : tests de charge sur catalogue et checkout (Locust/JMeter).

## 6. Synthèse pour stakeholder
- **Plateforme prête à supporter un MVP multi-rôle** (clients, vendeurs approuvés, admins).
- **Tunnels critiques testés** : panier → commande → facture → email, notifications vendeur/admin.
- **Documentation** : README (setup), docs features, test-report, project overview (ce document).
- **Évolutions prioritaires** : API coverage, scénarios d’échec, pipeline automatisé, conformité.

---
Document généré le `08/11/2025`. À tenir à jour en fonction des futures évolutions.

