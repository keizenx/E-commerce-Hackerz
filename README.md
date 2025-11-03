# Django Hackerz E-Commerce # Django Hackerz



![Django Hackerz Banner](https://img.shields.io/badge/Django-5.0.1-green.svg)Une plateforme e-commerce et blog sécurisée développée avec Django.



A sleek and modern e-commerce platform with multi-vendor support, built with Django.##  Fonctionnalités



[![Platform](https://img.shields.io/badge/Platform-Web-blue.svg)](https://www.djangoproject.com/)### E-commerce

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)- Système de panier d'achat

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)- Gestion des produits par catégories

[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/keizenx/E-commerce-Hackerz/pulls)- Interface vendeur

- Système d'avis et de notation

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API](#api) • [License](#license)- Processus de paiement sécurisé

- Gestion des commandes

---

### Blog

## ✨ Features- Articles avec système de catégories et tags

- Commentaires et réponses

### 🛍️ **E-Commerce Core**- Formatage riche du contenu

- **Product Catalog**: Browse products with advanced filtering by category, price, and availability- Interface d'administration

- **Shopping Cart**: Real-time cart management with quantity adjustments

- **Order Management**: Complete order processing with status tracking### Sécurité

- **Payment Integration**: Secure checkout process with invoice generation- Authentification utilisateur

- **Reviews & Ratings**: Customer feedback system with verified purchases- Gestion des rôles (admin, vendeur, client)

- Protection contre les attaques CSRF

### 👥 **Multi-Vendor System**- Validation des données

- **Vendor Dashboard**: Dedicated interface for sellers to manage their products

- **Smart Restrictions**: Vendors cannot purchase their own products (automatic UI adaptation)##  Technologies

- **Product Management**: Add, edit, and delete products with stock tracking

- **Sales Analytics**: Real-time statistics and performance metrics- Python 3.x

- **Approval System**: Admin verification for new vendors- Django

- SQLite (base de données)

### 💰 **Discount System**- HTML/CSS/JavaScript

- **Coupon Codes**: Create promotional codes with flexible rules- Bootstrap Icons

- **Discount Types**: Percentage or fixed amount discounts

- **Usage Limits**: Set maximum uses and expiration dates## 📦 Installation

- **Minimum Purchase**: Configure minimum order values for coupons

1. Clonez le dépôt :

### 📝 **Integrated Blog**```bash

- **Rich Content**: Markdown support for articles with syntax highlightinggit clone https://github.com/keizenx/Django_Hackerz.git

- **Comments System**: Threaded discussions on blog postscd Django_Hackerz

- **Categories & Tags**: Organize content for easy discovery```

- **SEO Friendly**: Optimized meta tags and URLs

2. Créez un environnement virtuel :

### 🔐 **Security & Authentication**```bash

- **User Management**: Registration with email confirmationpython -m venv venv

- **Two-Factor Authentication**: Optional 2FA for enhanced securitysource venv/bin/activate  # Linux/Mac

- **Role-Based Access**: Separate permissions for customers, vendors, and admins# ou

- **Profile System**: Customizable user profiles with shipping addressesvenv\Scripts\activate  # Windows

```

### 🎨 **Modern UI/UX**

- **Dark Theme**: Elegant dark mode interface throughout the application3. Installez les dépendances :

- **Responsive Design**: Seamless experience across all devices```bash

- **AJAX Integration**: Dynamic content loading without page refreshespip install -r requirements.txt

- **Real-time Notifications**: Instant feedback for user actions```



### 🔌 **REST API**4. Effectuez les migrations :

- **Full API Coverage**: Complete CRUD operations for all resources```bash

- **Token Authentication**: Secure API access with token-based authpython manage.py migrate

- **Interactive Documentation**: Auto-generated Swagger/ReDoc interface```

- **Filtering & Pagination**: Advanced query capabilities

5. Créez un superutilisateur :

---```bash

python manage.py createsuperuser

## 📦 Installation```



This application consists of a Django backend. Follow the steps below to get it running on your system.6. Lancez le serveur :

```bash

### **Option 1: Quick Start (Recommended)**python manage.py runserver

```

#### Prerequisites

Ensure you have the following installed:## 🔐 Configuration

- Python 3.12 or higher

- pip (Python package manager)1. Créez un fichier `.env` à la racine du projet

- Git2. Ajoutez les variables d'environnement nécessaires :

```env

#### StepsSECRET_KEY=votre_clé_secrète

DEBUG=True

1. **Clone the repository:**```

```bash

git clone https://github.com/keizenx/E-commerce-Hackerz.git## 👥 Contribution

cd E-commerce-Hackerz

```Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet

2. **Create and activate a virtual environment:**2. Créer une branche pour votre fonctionnalité

3. Commiter vos changements

On **Windows**:4. Pousser vers la branche

```bash5. Ouvrir une Pull Request

python -m venv venv

venv\Scripts\activate## 📝 Licence

```

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

On **Linux/Mac**:

```bash## 📧 Contact

python -m venv venv

source venv/bin/activate- Auteur : keizenx

```- GitHub : [@keizenx](https://github.com/keizenx)


3. **Install dependencies:**

For **development**:
```bash
pip install -r requirements-dev.txt
```

For **production**:
```bash
pip install -r requirements-prod.txt
```

For **basic setup** (minimal):
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
# - SECRET_KEY: Django secret key
# - DEBUG: Set to False in production
# - ALLOWED_HOSTS: Your domain names
# - DATABASE_URL: Database connection string
# - EMAIL_* : Email server configuration
```

5. **Run database migrations:**
```bash
python manage.py migrate
```

6. **Create a superuser account:**
```bash
python manage.py createsuperuser
```

7. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

8. **Run the development server:**
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### **Option 2: Docker Deployment (Coming Soon)**

```bash
# Build and run with Docker Compose
docker-compose up -d
```

---

## 🚀 Usage

### **Getting Started**

1. **Access the Application:**
   - **Homepage**: `http://127.0.0.1:8000/`
   - **Admin Panel**: `http://127.0.0.1:8000/admin/`
   - **Shop**: `http://127.0.0.1:8000/shop/`
   - **Blog**: `http://127.0.0.1:8000/blog/`

2. **User Roles:**
   - **Customer**: Browse products, make purchases, leave reviews
   - **Vendor**: Manage own products, view sales statistics
   - **Admin**: Full access to all features and user management

### **Vendor Features**

To become a vendor:
1. Register a regular account
2. Navigate to "Become a Vendor" in your profile
3. Fill out the vendor application form
4. Wait for admin approval
5. Access your vendor dashboard at `/vendor/products/`

**Vendor Dashboard:**
- **Add Products**: Upload images, set prices, manage stock
- **View Orders**: Track sales and customer purchases
- **Analytics**: Monitor product performance
- **Profile**: Update shop information and branding

### **Shopping Experience**

**Cart Management:**
- Add products to cart with quantity selection
- Update quantities or remove items
- Apply discount coupons at checkout
- Save products to wishlist for later

**Checkout Process:**
1. Review cart items and total
2. Enter shipping information
3. Apply coupon code (optional)
4. Confirm and place order
5. Receive order confirmation email with PDF invoice

### **Product Discovery**

- **Search**: Find products by name or description
- **Filter**: By category, price range, availability
- **Sort**: By price, newest, popularity
- **Reviews**: Read customer feedback before purchasing

---

## 🔌 API

The platform provides a complete REST API for programmatic access.

### **API Documentation**

Access interactive API documentation:
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

### **Authentication**

```bash
# Obtain authentication token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in subsequent requests
curl http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Token your_token_here"
```

### **Key Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products/` | GET | List all products |
| `/api/products/{id}/` | GET | Get product details |
| `/api/orders/` | GET, POST | List/create orders |
| `/api/cart/` | GET, POST | Manage shopping cart |
| `/api/reviews/` | GET, POST | Product reviews |
| `/api/coupons/validate/` | POST | Validate coupon code |

---

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test tests.unit.test_vendor_own_products

# Run with coverage report
pytest --cov=. --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

### **Test Coverage**

The project includes comprehensive tests for:
- ✅ Vendor restrictions (preventing self-purchase)
- ✅ Cart and checkout functionality
- ✅ Coupon validation and application
- ✅ Order processing
- ✅ API endpoints

---

## 📚 Documentation

Additional documentation is available in the `/docs` directory:

- **[Vendor Restrictions Guide](docs/features/vendor_restrictions.md)**: Detailed explanation of vendor limitations
- **[Testing Documentation](DOCUMENTATION_TESTS.md)**: How to write and run tests
- **API Examples**: Sample requests and responses

---

## 🛠️ Technology Stack

### **Backend**
- **Django 5.0.1**: Web framework
- **Django REST Framework**: API development
- **Pillow**: Image processing
- **xhtml2pdf**: PDF generation for invoices
- **Markdown**: Rich text content

### **Frontend**
- **HTML5/CSS3**: Markup and styling
- **JavaScript (ES6+)**: Client-side interactivity
- **Bootstrap Icons**: Icon library

### **Database**
- **SQLite**: Development (default)
- **PostgreSQL**: Production (recommended)

### **Development Tools**
- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Code linter
- **django-debug-toolbar**: Debugging

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### **Contribution Guidelines**

- Follow PEP 8 style guide for Python code
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Keizen**
- GitHub: [@keizenx](https://github.com/keizenx)
- Repository: [E-commerce-Hackerz](https://github.com/keizenx/E-commerce-Hackerz)

---

## 🙏 Acknowledgments

- Django community for the amazing framework
- Contributors and testers
- Open-source community

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/keizenx/E-commerce-Hackerz/issues)
3. Create a [new issue](https://github.com/keizenx/E-commerce-Hackerz/issues/new) with detailed information

---

⭐ **If you find this project useful, please consider giving it a star on GitHub!**
