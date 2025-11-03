# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Hackerz_E_commerce.models import Product, Category
from Hackerz.models import Vendor, Profile
from django.utils.text import slugify
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Peuple la boutique avec des produits réalistes'

    def handle(self, *args, **options):
        self.stdout.write("🛒 Début de la population de la boutique...")

        # Récupérer ou créer un vendeur
        try:
            vendor_user = User.objects.filter(profile__vendor__isnull=False).first()
            if not vendor_user:
                # Créer un utilisateur vendeur
                vendor_user = User.objects.create_user(
                    username='vendeur_principal',
                    email='vendeur@hackerz.com',
                    password='vendeur123',
                    first_name='Franck',
                    last_name='Vendeur'
                )
                profile = Profile.objects.get(user=vendor_user)
                vendor = Vendor.objects.create(
                    profile=profile,
                    shop_name='HackerZ Electronics',
                    description='Le meilleur de la tech à prix compétitifs',
                    is_approved=True
                )
                self.stdout.write(self.style.SUCCESS("✅ Vendeur créé: HackerZ Electronics"))
            else:
                vendor = vendor_user.profile.vendor
                self.stdout.write(self.style.SUCCESS(f"✅ Vendeur existant: {vendor.shop_name}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur vendeur: {e}"))
            return

        # === CATÉGORIES ===
        self.stdout.write("\n📂 Création des catégories...")
        
        categories_data = [
            ('peripheriques', 'Périphériques', 'Claviers, souris, webcams...'),
            ('composants', 'Composants PC', 'Processeurs, cartes mères, RAM...'),
            ('audio', 'Audio & Casques', 'Casques, enceintes, micros...'),
            ('gaming', 'Gaming', 'Matériel spécifique gaming'),
            ('stockage', 'Stockage', 'SSD, HDD, clés USB...'),
            ('ecrans', 'Écrans', 'Moniteurs, TV, projecteurs...'),
            ('reseau', 'Réseau', 'Routeurs, switches, câbles...'),
            ('accessoires', 'Accessoires', 'Housses, câbles, adaptateurs...'),
        ]

        created_categories = {}
        for slug, name, desc in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc}
            )
            created_categories[slug] = category
            status = "✨ créée" if created else "✓ existante"
            self.stdout.write(f"  {status}: {name}")

        self.stdout.write(self.style.SUCCESS(f"✅ {len(created_categories)} catégories"))

        # === PRODUITS ===
        self.stdout.write("\n🎁 Création des produits...")
        
        products_data = [
            # Périphériques
            ('Clavier Mécanique RGB Pro Gaming', 'peripheriques', 129.99, 149.99, 45, True, True),
            ('Souris Gaming Sans Fil 16000 DPI', 'peripheriques', 79.99, 99.99, 62, True, True),
            ('Webcam 4K Pro Streaming', 'peripheriques', 149.99, 189.99, 28, True, False),
            ('Clavier Bureau Ergonomique Silent', 'peripheriques', 49.99, 69.99, 85, True, False),
            ('Souris Verticale Ergonomique', 'peripheriques', 39.99, 54.99, 42, True, False),
            ('Trackball Pro Designer', 'peripheriques', 89.99, 119.99, 15, True, False),
            ('Pavé Numérique Sans Fil', 'peripheriques', 24.99, 34.99, 55, True, False),
            
            # Audio
            ('Casque Gaming RGB 7.1 Surround', 'audio', 89.99, 129.99, 38, True, True),
            ('Casque Bluetooth ANC Premium', 'audio', 249.99, 299.99, 22, True, True),
            ('Micro USB Streaming Pro', 'audio', 119.99, 149.99, 31, True, False),
            ('Enceintes 2.1 Bluetooth 60W', 'audio', 79.99, 99.99, 44, True, False),
            ('Micro XLR Studio Professionnel', 'audio', 199.99, 259.99, 12, True, False),
            ('Écouteurs True Wireless Sport', 'audio', 69.99, 89.99, 58, True, True),
            ('Casque Studio Monitoring', 'audio', 159.99, 199.99, 18, True, False),
            
            # Stockage
            ('SSD NVMe 1To Gen4', 'stockage', 99.99, 129.99, 120, True, True),
            ('SSD NVMe 2To Gen4', 'stockage', 179.99, 229.99, 68, True, False),
            ('HDD Externe 4To USB 3.2', 'stockage', 89.99, 119.99, 92, True, False),
            ('Clé USB 3.0 256Go', 'stockage', 29.99, 39.99, 150, True, False),
            ('SSD Portable 1To USB-C', 'stockage', 119.99, 149.99, 45, True, True),
            ('NAS 2 Baies + 2x4To', 'stockage', 449.99, 549.99, 8, True, False),
            
            # Écrans
            ('Écran Gaming 27" 165Hz QHD', 'ecrans', 299.99, 399.99, 34, True, True),
            ('Écran 24" Full HD IPS', 'ecrans', 149.99, 199.99, 56, True, False),
            ('Écran 32" 4K UHD HDR', 'ecrans', 449.99, 599.99, 18, True, False),
            ('Écran Portable 15.6" USB-C', 'ecrans', 179.99, 229.99, 28, True, False),
            ('Écran Incurvé 34" Ultrawide', 'ecrans', 599.99, 749.99, 12, True, True),
            
            # Gaming
            ('Manette Pro Sans Fil RGB', 'gaming', 59.99, 79.99, 75, True, True),
            ('Volant + Pédales Racing Simulator', 'gaming', 249.99, 319.99, 15, True, False),
            ('Tapis de Souris Gaming XXL RGB', 'gaming', 34.99, 49.99, 88, True, False),
            ('Chaise Gaming Pro Ergonomique', 'gaming', 299.99, 399.99, 22, True, True),
            ('Support Casque RGB', 'gaming', 24.99, 34.99, 65, True, False),
            ('Stream Deck Mini', 'gaming', 79.99, 99.99, 35, True, False),
            
            # Composants
            ('RAM DDR5 32Go (2x16) 6000MHz', 'composants', 149.99, 199.99, 42, True, False),
            ('Carte Graphique RTX 4070 12Go', 'composants', 649.99, 749.99, 8, True, True),
            ('Processeur Intel i7-14700K', 'composants', 399.99, 479.99, 18, True, False),
            ('Carte Mère B760 ATX WiFi', 'composants', 189.99, 239.99, 25, True, False),
            ('Alimentation 750W Gold Modulaire', 'composants', 109.99, 139.99, 38, True, False),
            ('Ventirad RGB 240mm AIO', 'composants', 119.99, 149.99, 28, True, False),
            ('Boîtier ATX RGB Verre Trempé', 'composants', 89.99, 119.99, 32, True, False),
            
            # Réseau
            ('Routeur WiFi 6 AX3000', 'reseau', 89.99, 129.99, 45, True, False),
            ('Switch Gigabit 8 Ports', 'reseau', 34.99, 49.99, 62, True, False),
            ('Carte Réseau PCIe WiFi 6E', 'reseau', 49.99, 69.99, 38, True, False),
            ('Répéteur WiFi 6 Mesh', 'reseau', 79.99, 99.99, 52, True, False),
            
            # Accessoires
            ('Hub USB-C 7-en-1', 'accessoires', 39.99, 54.99, 95, True, True),
            ('Câble HDMI 2.1 8K 2m', 'accessoires', 19.99, 29.99, 150, True, False),
            ('Support PC Portable Aluminium', 'accessoires', 29.99, 39.99, 75, True, False),
            ('Bras Écran Articulé Double', 'accessoires', 89.99, 119.99, 32, True, False),
            ('Station Charge USB Multiple', 'accessoires', 44.99, 59.99, 58, True, False),
            ('Multiprise Parafoudre 10 Prises', 'accessoires', 34.99, 44.99, 82, True, False),
            ('Lampe LED Bureau USB', 'accessoires', 24.99, 34.99, 68, True, False),
        ]

        created_count = 0
        featured_count = 0
        
        for name, cat_slug, price, regular, stock, available, featured in products_data:
            try:
                category = created_categories[cat_slug]
                
                # Générer slug unique
                base_slug = slugify(name)
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Description automatique
                desc = f"{name} - Produit de qualité professionnelle avec garantie fabricant."
                
                product, created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'name': name,
                        'category': category,
                        'vendor': vendor,
                        'description': desc,
                        'price': Decimal(str(price)),
                        'regular_price': Decimal(str(regular)),
                        'stock': stock,
                        'available': available,
                        'featured': featured
                    }
                )
                
                if created:
                    created_count += 1
                    if featured:
                        featured_count += 1
                    status = "✨"
                else:
                    status = "✓"
                
                self.stdout.write(f"  {status} {name}")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Erreur: {name} - {e}"))

        # === STATISTIQUES ===
        self.stdout.write("\n" + "="*60)
        self.stdout.write("📊 RÉSUMÉ DE LA BOUTIQUE")
        self.stdout.write("="*60)
        self.stdout.write(f"🏪 Vendeur: {vendor.shop_name}")
        self.stdout.write(f"📂 Catégories: {Category.objects.count()}")
        self.stdout.write(f"📦 Produits totaux: {Product.objects.count()}")
        self.stdout.write(f"🆕 Nouveaux produits: {created_count}")
        self.stdout.write(f"⭐ Produits featured: {Product.objects.filter(featured=True).count()}")
        self.stdout.write(f"✅ Produits disponibles: {Product.objects.filter(available=True).count()}")
        self.stdout.write("="*60)
        self.stdout.write(self.style.SUCCESS("✅ Population boutique terminée !"))
        self.stdout.write("\n💡 Voir la boutique : http://localhost:8000/shop/")
