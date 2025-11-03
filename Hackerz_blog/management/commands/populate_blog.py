# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Hackerz_blog.models import Post, Category, Tag
from django.utils.text import slugify
from django.utils import timezone


class Command(BaseCommand):
    help = 'Peuple le blog avec des articles et tags'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Début de la population du blog...")

        # Récupérer ou créer un auteur
        try:
            author = User.objects.filter(is_staff=True).first()
            if not author:
                author = User.objects.create_user(
                    username='admin_blog',
                    email='blog@hackerz.com',
                    password='admin123',
                    is_staff=True
                )
                self.stdout.write(self.style.SUCCESS("✅ Auteur créé: admin_blog"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ Auteur existant: {author.username}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur création auteur: {e}"))
            author = User.objects.first()

        # === TAGS ===
        self.stdout.write("\n📌 Création des tags...")
        
        tags_data = {
            'gaming': 'Gaming et jeux vidéo',
            'professionnel': 'Usage professionnel',
            'bureautique': 'Bureautique et productivité',
            'multimedia': 'Multimédia',
            'audio': 'Audio et son',
            'video': 'Vidéo et image',
            'stockage': 'Stockage et disques',
            'reseau': 'Réseau et connectivité',
            'peripheriques': 'Périphériques',
            'travail-domicile': 'Travail à domicile',
            'etudiant': 'Pour étudiants',
            'creator': 'Création de contenu',
            'developpeur': 'Développement',
            'streaming': 'Streaming',
            'guide-achat': 'Guide d\'achat',
            'tutoriel': 'Tutoriel',
            'comparatif': 'Comparatif produits',
            'actualite': 'Actualités tech',
            'test-produit': 'Test de produit',
            'conseils': 'Conseils pratiques',
            'top-liste': 'Top listes',
            'tendance': 'Tendances',
            'nouveaute': 'Nouveautés',
            'review': 'Avis et reviews',
        }

        created_tags = {}
        for tag_slug, tag_name in tags_data.items():
            tag, created = Tag.objects.get_or_create(
                slug=tag_slug,
                defaults={'name': tag_name}
            )
            created_tags[tag_slug] = tag
            status = "✨ créé" if created else "✓ existant"
            self.stdout.write(f"  {status}: {tag_name}")

        self.stdout.write(self.style.SUCCESS(f"✅ {len(created_tags)} tags disponibles"))

        # === CATÉGORIES ===
        self.stdout.write("\n📂 Création des catégories...")
        
        categories_data = [
            ('guides', 'Guides & Tutoriels', 'Guides complets et tutoriels pratiques'),
            ('actualites', 'Actualités Tech', 'Les dernières nouvelles du monde tech'),
            ('reviews', 'Tests & Reviews', 'Nos tests et avis détaillés'),
            ('conseils', 'Conseils', 'Astuces et conseils pour mieux acheter'),
            ('communaute', 'Communauté', 'Histoires et témoignages de notre communauté'),
        ]

        created_categories = {}
        for cat_slug, cat_name, cat_desc in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_slug,
                defaults={'name': cat_name, 'description': cat_desc}
            )
            created_categories[cat_slug] = category
            status = "✨ créée" if created else "✓ existante"
            self.stdout.write(f"  {status}: {cat_name}")

        self.stdout.write(self.style.SUCCESS(f"✅ {len(created_categories)} catégories disponibles"))

        # === ARTICLES ===
        self.stdout.write("\n📝 Création des articles...")
        
        articles = [
            {
                'title': 'Guide d\'achat 2025 : Comment choisir son matériel informatique',
                'category': 'guides',
                'tags': ['guide-achat', 'conseils', 'professionnel'],
                'content': 'Introduction\n\nChoisir le bon matériel informatique...',
                'status': 'published'
            },
            # Ajoutez les autres articles ici...
        ]

        created_posts = 0
        for i, article_data in enumerate(articles, 1):
            try:
                base_slug = slugify(article_data['title'])
                slug = base_slug
                counter = 1
                while Post.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                post = Post.objects.create(
                    title=article_data['title'],
                    slug=slug,
                    author=author,
                    category=created_categories[article_data['category']],
                    content=article_data['content'],
                    status=article_data['status'],
                    publish=timezone.now()
                )
                
                for tag_slug in article_data['tags']:
                    if tag_slug in created_tags:
                        post.tags.add(created_tags[tag_slug])
                
                created_posts += 1
                self.stdout.write(f"  ✨ Article {i}/{len(articles)}: {post.title[:50]}...")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Erreur article {i}: {e}"))

        # === STATISTIQUES ===
        self.stdout.write("\n" + "="*60)
        self.stdout.write("📊 RÉSUMÉ")
        self.stdout.write("="*60)
        self.stdout.write(f"👤 Auteur: {author.username}")
        self.stdout.write(f"🏷️  Tags: {Tag.objects.count()}")
        self.stdout.write(f"📂 Catégories: {Category.objects.count()}")
        self.stdout.write(f"📝 Articles: {Post.objects.count()}")
        self.stdout.write("="*60)
        self.stdout.write(self.style.SUCCESS("✅ Population terminée !"))
